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
import re

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
    """
    client_ip = request.headers.get('x-forwarded-for', request.remote_addr)
    if not check_rate_limit(client_ip):
        return jsonify({"error": "Muitas requisições. Tente novamente em 1 minuto."}), 429
    
    data = request.get_json()
    email_content = data.get('email_content', '').strip()

    if not email_content:
        return jsonify({"error": "Conteúdo do email não fornecido."}), 400

    # *** MUDANÇA 1: Lógica de Classificação mais Robusta ***
    # Adicionamos palavras-chave para ajudar a "desempatar" e corrigir a IA.
    palavras_chave_produtivas = ["status", "ticket", "problema", "ajuda", "solicito", "dúvida", "preciso"]
    palavras_chave_improdutivas = ["obrigado", "obrigada", "agradeço", "parabéns", "excelente", "ótimo"]

    # Primeiro, verificamos as palavras-chave para uma decisão rápida
    if any(palavra in email_content.lower() for palavra in palavras_chave_improdutivas):
        categoria_final = "Improdutivo"
    elif any(palavra in email_content.lower() for palavra in palavras_chave_produtivas):
        categoria_final = "Produtivo"
    else:
        # Se não houver palavras-chave, aí sim usamos a IA como desempate
        candidate_labels = ["e-mail de trabalho que necessita de uma ação", "e-mail casual de agradecimento"]
        classification_results = classifier(email_content, candidate_labels)
        top_label = classification_results['labels'][0]
        categoria_final = "Produtivo" if "ação" in top_label else "Improdutivo"

    # *** MUDANÇA 2: Respostas pré-definidas para garantir a qualidade ***
    # Em vez de gerar texto, usamos respostas prontas e confiáveis.
    # Isso elimina completamente o problema de respostas em inglês ou sem sentido.
    if categoria_final == "Produtivo":
        resposta_sugerida = "Prezado(a), recebemos sua mensagem e nossa equipe já está verificando a sua solicitação. Retornaremos o mais breve possível."
    else: # Improdutivo
        resposta_sugerida = "Prezado(a), agradecemos o seu contato e ficamos felizes em ajudar. Tenha um ótimo dia!"

    return jsonify({
        "categoria": categoria_final,
        "resposta_sugerida": resposta_sugerida,
        # Mantemos a saída da IA para debug, caso a tenhamos usado
        "raw_classification": locals().get('classification_results', 'Decisão por palavra-chave') 
    })

if __name__ == '__main__':
    app.run(debug=True)