import requests
import json

# URL da sua API Flask
API_URL = "http://127.0.0.1:5000/classificar"

def send_email_for_classification(email_content):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email_content": email_content
    }
    
    print(f"\nEnviando email para classificação:\n---{email_content}---\n")
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Lança um erro para status de erro HTTP
        
        result = response.json()
        print("\n--- Resultado da Classificação ---")
        print(f"Categoria: {result.get('categoria')}")
        print(f"Resposta Sugerida: {result.get('resposta_sugerida')}")
        # print(f"Classificação Bruta: {json.dumps(result.get('raw_classification'), indent=2)}") # Descomente para ver detalhes
        print("----------------------------------")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ou receber resposta do servidor: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Corpo da Resposta: {e.response.text}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON da resposta: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    # Certifique-se de que seu servidor Flask (app.py) está rodando!

    # Exemplo 1: Email produtivo
    email_produtivo = "Prezados, favor me atualizar sobre o status do projeto X até o final do dia. É urgente. Grato."
    send_email_for_classification(email_produtivo)

    # Exemplo 2: Email improdutivo
    email_improdutivo = "Olá equipe! Desejo a todos um excelente final de semana! Abs!"
    send_email_for_classification(email_improdutivo)

    # Exemplo 3: Outro email produtivo
    email_produtivo_2 = "Preciso de suporte técnico para o sistema de RH. Meu login não está funcionando. Por favor, me ajudem o mais rápido possível."
    send_email_for_classification(email_produtivo_2)

    # Exemplo 4: Outro email improdutivo
    email_improdutivo_2 = "Parabéns pelo excelente trabalho no último projeto! Fico muito feliz com os resultados. Abraços."
    send_email_for_classification(email_improdutivo_2)

    # Exemplo 5: Email com conteúdo vazio (para testar tratamento de erro)
    email_vazio = ""
    send_email_for_classification(email_vazio)