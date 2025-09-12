# 🤖 AutoAI: Classificador de Email com IA

## Visão Geral do Projeto

Este projeto demonstra uma aplicação web minimalista e eficiente para classificação automática de e-mails e sugestão de respostas, utilizando o poder da Inteligência Artificial. Desenvolvido com Flask para o backend e uma interface web moderna com Bulma CSS e JavaScript no frontend, o **AutoAI** oferece uma solução prática para gerenciar o fluxo de mensagens, categorizando-as como 'Produtivas' ou 'Improdutivas' e fornecendo respostas contextuais.

O objetivo principal é otimizar a triagem de e-mails, permitindo que usuários ou equipes de suporte respondam de forma mais rápida e consistente, liberando tempo para tarefas de maior complexidade.

## Demonstração do Projeto

Uma prévia visual da aplicação em funcionamento:

![https://autoai-email-classifier.onrender.com](img/AutoAI.png)

## 🚀 Aplicação Online

A versão de produção desta aplicação está hospedada no Render e pode ser acessada através do seguinte link:

**[https://autoai-email-classifier.onrender.com]**

## Funcionalidades Chave

-   **Classificação Inteligente:** Utiliza um modelo de `zero-shot classification` da Hugging Face (`facebook/bart-large-mnli`) para categorizar e-mails sem a necessidade de treinamento prévio com dados específicos do domínio.
-   **Sugestão de Respostas:** Gera respostas automáticas e contextuais baseadas na classificação do e-mail, utilizando um modelo de `text-generation` (`gpt2`).
-   **Interface Amigável:** Design responsivo e intuitivo, permitindo a inserção de e-mails via digitação de texto ou upload de arquivo `.txt`.
-   **Animações de Carregamento:** Feedback visual durante o processamento da IA para uma melhor experiência do usuário.
-   **Design Robusto:** Layout com rodapé fixo e elementos centralizados para uma estética profissional.
-   **Medidas de Segurança Implementadas:**
    -   **Rate Limiting (Flask-Limiter):** Proteção contra abuso e ataques de negação de serviço (DoS) na API de classificação, limitando o número de requisições por IP.
    -   **HTTPS Automático:** Garantido pela plataforma de deploy (Render), assegura que toda a comunicação é criptografada.
    -   **Servidor de Produção (Gunicorn):** Uso de um servidor WSGI seguro para deploy, desativando o modo de depuração em ambiente de produção.

## Tecnologias Utilizadas

-   **Backend:** Python 3.x, Flask
-   **Inteligência Artificial:** Hugging Face Transformers (Zero-shot Classification com BART, Text Generation com GPT-2)
-   **Frontend:** HTML5, CSS3 (Bulma Framework), JavaScript
-   **Segurança:** Flask-Limiter
-   **Servidor de Produção:** Gunicorn
-   **Hospagem:** Render.com
-   **Controle de Versão:** Git & GitHub

## Como Rodar o Projeto Localmente

Siga estes passos para configurar e executar a aplicação em sua máquina local:

### Pré-requisitos

-   Python 3.x instalado
-   pip (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/MatheusdePaulo/AutoAI-email-classifier.git](https://github.com/MatheusdePaulo/AutoAI-email-classifier.git)
    cd AutoAI-email-classifier
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Executando a Aplicação

1.  Com o ambiente virtual ativado, execute o servidor Flask:
    ```bash
    python app.py
    ```

2.  Abra seu navegador e acesse: `http://127.0.0.1:5000/`

## Deploy na Nuvem (Render.com)

A aplicação está configurada para ser facilmente implantada em plataformas como o Render.com. O deploy é automatizado através de:

-   `requirements.txt`: Lista de dependências Python.
-   `Procfile`: Define o comando de inicialização do servidor (Gunicorn).
-   `runtime.txt`: Especifica a versão do Python.

Para implantar no Render, conecte seu repositório GitHub e configure um "Web Service", usando as configurações detectadas automaticamente.

---

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

---

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes. *(Você precisaria criar um arquivo LICENSE separadamente se desejar)*