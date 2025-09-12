from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configuração do Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "10 per minute"],
    storage_uri="memory://",
    headers_enabled=True
)

# --- Configuração da IA (Apenas o Classificador) ---
try:
    # Mantemos apenas o modelo de classificação, que é mais leve
    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
except Exception as e:
    print(f"Erro ao carregar modelo da Hugging Face: {e}")
    classifier = None

# --- Rotas da Aplicação ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classificar', methods=['POST'])
@limiter.limit("5/minute")
def classificar_email():
    if not classifier:
        return jsonify({"error": "Modelo de IA não carregado."}), 500

    data = request.get_json()
    if not data:
        data = request.form
        
    email_content = data.get('email_content', '').strip()

    if not email_content:
        return jsonify({"error": "Conteúdo do email não fornecido."}), 400

    # --- Lógica de Classificação com IA ---
    candidate_labels = ["solicitação de ação", "atualização de status", "problema técnico", 
                        "informação geral", "agradecimento", "cumprimento"]
    
    classification_results = classifier(email_content, candidate_labels, multi_label=True)
    
    label_mapping = {
        "solicitação de ação": "Produtivo",
        "atualização de status": "Produtivo",
        "problema técnico": "Produtivo",
        "informação geral": "Improdutivo",
        "agradecimento": "Improdutivo",
        "cumprimento": "Improdutivo"
    }

    categoria_final = "Não Classificado"
    max_score = 0.0
    
    for label, score in zip(classification_results['labels'], classification_results['scores']):
        if score > max_score and label in label_mapping:
            max_score = score
            categoria_final = label_mapping[label]
    
    if max_score < 0.4: # Aumentando um pouco a exigência de confiança
        categoria_final = "Não Classificado"

    # --- Lógica de Geração de Resposta (SEM IA, baseada em templates) ---
    if categoria_final == "Produtivo":
        resposta_sugerida = (
            "Prezado(a),\n\n"
            "Recebemos sua mensagem e já estamos analisando o conteúdo.\n"
            "Em breve retornaremos com mais informações sobre sua solicitação.\n\n"
            "Atenciosamente,\nEquipe de Automação"
        )
    elif categoria_final == "Improdutivo":
        resposta_sugerida = (
            "Prezado(a),\n\n"
            "Agradecemos o seu contato e a sua mensagem!\n\n"
            "Tenha um excelente dia.\n\n"
            "Atenciosamente,\nEquipe de Automação"
        )
    else: # "Não Classificado"
        resposta_sugerida = (
            "Prezado(a),\n\n"
            "Sua mensagem foi recebida com sucesso.\n"
            "Um de nossos atendentes irá revisá-la e responder em breve.\n\n"
            "Atenciosamente,\nEquipe de Automação"
        )
    
    return jsonify({
        "categoria": categoria_final,
        "resposta_sugerida": resposta_sugerida,
        "email_recebido": email_content,
        "raw_classification": classification_results
    })

if __name__ == '__main__':
    app.run(debug=True)