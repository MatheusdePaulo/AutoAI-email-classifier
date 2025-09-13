"""
Aplicação Flask para classificação de e-mails com Inteligência Artificial.

Esta aplicação web permite que os usuários insiram o conteúdo de um e-mail
via texto ou upload de arquivo .txt. O conteúdo é então processado por
dois modelos de IA da Hugging Face:
1. Um modelo de Zero-Shot Classification para categorizar o e-mail.
2. Um modelo de Text Generation para sugerir uma resposta apropriada.

A aplicação inclui um sistema de rate limiting para prevenir abusos e
é projetada para ser implantada como um contêiner Docker.
"""
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import time
import re # Importa a biblioteca de expressões regulares

app = Flask(__name__)

# --- Rate Limiting Manual Simples ---
request_times = {}
MAX_REQUESTS_PER_MINUTE = 5

def check_rate_limit(ip):
    current_time = time.time()
    if ip in request_times:
        requests = [t for t in request_times[ip] if current_time - t < 60]
        if len(requests) >= MAX_REQUESTS_PER_MINUTE:
            return False
        requests.append(current_time)
        request_times[ip] = requests
    else:
        request_times[ip] = [current_time]
    return True

# --- Configuração da IA ---
# Usamos um modelo mais robusto e multilíngue para melhor entendimento.
classifier = pipeline("zero-shot-classification", 
                      model="facebook/bart-large-mnli")

text_generator = pipeline("text-generation", 
                          model="distilgpt2")

@app.route('/')
def index():
    """Renderiza a página inicial da aplicação (index.html)."""
    return render_template('index.html')

@app.route('/classificar', methods=['POST'])
def classificar_email():
    """
    Recebe o conteúdo de um e-mail via POST, classifica-o usando um modelo
    de zero-shot e gera uma resposta sugerida.

    A requisição deve ser um JSON com a chave 'email_content'.
    Aplica-se um limite de requisições por IP.

    Returns:
        JSON: Um objeto contendo a categoria, a resposta sugerida e
              os dados brutos da classificação.
        JSON, status 429: Se o limite de requisições for excedido.
        JSON, status 400: Se o conteúdo do e-mail não for fornecido.
    """
    # Verificação de Rate Limit
    client_ip = request.headers.get('x-forwarded-for', request.remote_addr)
    if not check_rate_limit(client_ip):
        return jsonify({"error": "Muitas requisições. Tente novamente em 1 minuto."}), 429
    
    data = request.get_json()
    email_content = data.get('email_content', '').strip()

    if not email_content:
        return jsonify({"error": "Conteúdo do email não fornecido."}), 400

    # *** MUDANÇA 1: Rótulos mais descritivos para ajudar a IA ***
    candidate_labels = [
        "e-mail de trabalho que necessita de uma ação ou resposta técnica", 
        "e-mail casual, agradecimento ou cumprimento que não precisa de ação"
    ]
    
    # Usamos uma hipótese para guiar o modelo, tornando-o mais preciso
    hypothesis_template = "O tópico deste e-mail é {}."
    classification_results = classifier(email_content, candidate_labels, hypothesis_template=hypothesis_template)
    
    # Determina a categoria com base no rótulo de maior pontuação
    top_label = classification_results['labels'][0]
    
    if "necessita de uma ação" in top_label:
        categoria_final = "Produtivo"
    else:
        categoria_final = "Improdutivo"

    # Define o prompt para a geração de texto
    if categoria_final == "Produtivo":
        prompt_prefix = "Escreva uma resposta profissional curta para um e-mail de trabalho que precisa de ação, começando com 'Prezado(a), recebemos sua mensagem e estamos verificando'."
    else:
        prompt_prefix = "Escreva uma resposta profissional curta e amigável para um e-mail de trabalho que não precisa de ação, começando com 'Prezado(a), agradecemos o contato!'."
    
    generated_text_raw = text_generator(
        prompt_prefix,
        max_new_tokens=50, # Aumentamos um pouco para dar mais espaço
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
        pad_token_id=text_generator.tokenizer.eos_token_id # Evita warnings
    )[0]['generated_text']

    # *** MUDANÇA 2: Limpeza e formatação da resposta da IA ***
    # Remove o prompt inicial da resposta gerada
    resposta_limpa = generated_text_raw.replace(prompt_prefix, "").strip()
    
    # Usa expressão regular para pegar apenas a primeira frase completa
    match = re.search(r"^(.*?[\.\!\?])", resposta_limpa)
    if match:
        resposta_sugerida = match.group(1)
    else:
        resposta_sugerida = resposta_limpa # Usa a resposta limpa se não encontrar uma frase completa

    return jsonify({
        "categoria": categoria_final,
        "resposta_sugerida": resposta_sugerida,
        "raw_classification": classification_results
    })

if __name__ == '__main__':
    app.run(debug=True)