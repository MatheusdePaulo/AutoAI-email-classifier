from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import os
import time

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
# --- Fim do Rate Limiting ---

# --- Configuração da IA ---
classifier = pipeline("zero-shot-classification", 
                     model="typeform/distilbert-base-uncased-mnli")

text_generator = pipeline("text-generation", 
                         model="distilgpt2")

# --- Rotas ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classificar', methods=['POST'])
def classificar_email():
    # Verificação de Rate Limit
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return jsonify({"error": "Muitas requisições. Tente novamente em 1 minuto."}), 429
    
    if not classifier or not text_generator:
        return jsonify({"error": "Modelos de IA não carregados."}), 500

    data = request.get_json()
    if not data:
        data = request.form
        
    email_content = data.get('email_content', '').strip()

    if not email_content:
        return jsonify({"error": "Conteúdo do email não fornecido."}), 400

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
    
    if max_score < 0.4:
        categoria_final = "Não Classificado"

    prompt_prefix = ""
    if categoria_final == "Produtivo":
        prompt_prefix = "Escreva uma resposta profissional curta para um e-mail de trabalho que precisa de ação, começando com 'Prezado(a), recebemos sua mensagem e estamos verificando'."
    else:
        prompt_prefix = "Escreva uma resposta profissional curta e amigável para um e-mail de trabalho que não precisa de ação, começando com 'Prezado(a), agradecemos o contato!'."
    
    generated_text = text_generator(
        prompt_prefix,
        max_new_tokens=40,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7
    )[0]['generated_text']

    resposta_sugerida = generated_text

    return jsonify({
        "categoria": categoria_final,
        "resposta_sugerida": resposta_sugerida,
        "email_recebido": email_content,
        "raw_classification": classification_results
    })

if __name__ == '__main__':
    app.run(debug=True)