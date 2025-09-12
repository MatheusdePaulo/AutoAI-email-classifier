from flask import Flask, request, jsonify, render_template
from transformers import pipeline
# --- Importação do Flask-Limiter ---
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# --- Configuração do Limiter ---
# O Limiter vai usar o endereço IP remoto para identificar o usuário.
# default_limits: Limites aplicados a todas as rotas por padrão, se não forem sobrescritos.
#                 "200 por dia" - 200 requisições a cada 24 horas.
#                 "10 por minuto" - 10 requisições a cada 60 segundos.
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "10 per minute"], # <--- CORRIGIDO
    storage_uri="memory://",
    headers_enabled=True
)

# --- Configuração da IA (Carregar modelos apenas uma vez) ---
try:
    # Para deploy, é altamente recomendado carregar modelos localmente ou via cache
    # pois o download a cada reinício pode ser lento e consumir banda.
    # Se você for usar um ambiente sem internet (como algumas configs de deploy),
    # certifique-se de baixar e cachear esses modelos antes.
    # Classificador Zero-shot baseado em DistilBERT, mais leve
    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
    # Gerador de texto DistilGPT2
    text_generator = pipeline("text-generation", model="distilgpt2")
except Exception as e:
    print(f"Erro ao carregar modelos da Hugging Face: {e}")
    print("Certifique-se de ter uma conexão com a internet ou de que os modelos estão em cache.")
    classifier = None
    text_generator = None

# --- Rotas da Aplicação ---
# Rota principal para servir a interface HTML
@app.route('/')
def index():
    return render_template('index.html') # Renderiza o nosso arquivo HTML

# Aplicamos o limite diretamente na rota da API de classificação.
# "5/minute": Permite no máximo 5 requisições por minuto para esta rota específica.
# Este é um limite mais restrito porque é a rota que consome mais recursos de IA.
@app.route('/classificar', methods=['POST'])
@limiter.limit("5/minute") # <--- AQUI ESTÁ A IMPLEMENTAÇÃO DO RATE LIMITING!
def classificar_email():
    if not classifier or not text_generator:
        return jsonify({"error": "Modelos de IA não carregados. Verifique a instalação ou conexão."}), 500

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            data = request.form
            
        email_content = data.get('email_content', '').strip()

        if not email_content:
            return jsonify({"error": "Conteúdo do email não fornecido."}), 400

        # --- Lógica de Classificação com Zero-Shot Classification Refinada ---
        candidate_labels = ["solicitação de ação", "atualização de status", "problema técnico", 
                            "informação geral", "agradecimento", "cumprimento", "feliz natal"]
        
        classification_results = classifier(email_content, candidate_labels, multi_label=True)
        
        label_mapping = {
            "solicitação de ação": "Produtivo",
            "atualização de status": "Produtivo",
            "problema técnico": "Produtivo",
            "informação geral": "Improdutivo",
            "agradecimento": "Improdutivo",
            "cumprimento": "Improdutivo",
            "feliz natal": "Improdutivo"
        }

        categoria_final = "Não Classificado"
        max_score = 0.0
        
        for label, score in zip(classification_results['labels'], classification_results['scores']):
            if score > max_score:
                if label in label_mapping:
                    max_score = score
                    categoria_final = label_mapping[label]
        
        if max_score < 0.5 and categoria_final == "Não Classificado":
            categoria_final = "Improdutivo"

        # --- Lógica de Geração de Resposta Otimizada ---
        base_response = ""
        if categoria_final == "Produtivo":
            base_response = (
                "Prezado(a),\n"
                "Recebemos sua mensagem e já estamos analisando o conteúdo. "
                "Em breve retornaremos com mais informações ou a solução para sua solicitação."
            )
        elif categoria_final == "Improdutivo":
            base_response = (
                "Prezado(a),\n"
                "Agradecemos o seu contato e a sua mensagem! "
                "Tenha um excelente dia."
            )
        else: # "Não Classificado" ou fallback
            base_response = (
                "Prezado(a),\n"
                "Sua mensagem foi recebida. No momento, não conseguimos classificá-la automaticamente. "
                "Um de nossos atendentes irá revisá-la em breve."
            )
        
        resposta_sugerida = base_response

        return jsonify({
            "categoria": categoria_final,
            "resposta_sugerida": resposta_sugerida,
            "email_recebido": email_content,
            "raw_classification": classification_results # Para debug
        })

if __name__ == '__main__':
    # NUNCA USE debug=True EM AMBIENTE DE PRODUÇÃO!
    # Para deploy, usaremos Gunicorn e um Procfile.
    app.run(debug=True)