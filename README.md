---
title: AutoAI Email Classifier
emoji: 🤖
colorFrom: green
colorTo: blue
sdk: docker
app_port: 8000
---

# 🤖 AutoAI: Classificador de Email com IA

## Visão Geral do Projeto

Este projeto demonstra uma aplicação web minimalista e eficiente para classificação automática de e-mails e sugestão de respostas, utilizando o poder da Inteligência Artificial. Desenvolvido com Flask para o backend e uma interface web moderna com Bulma CSS e JavaScript no frontend, o **AutoAI** oferece uma solução prática para gerenciar o fluxo de mensagens, categorizando-as como 'Produtivas' ou 'Improdutivas' e fornecendo respostas contextuais.

O objetivo principal é otimizar a triagem de e-mails, permitindo que usuários ou equipes de suporte respondam de forma mais rápida e consistente, liberando tempo para tarefas de maior complexidade.

## Demonstração do Projeto

Uma prévia visual da aplicação em funcionamento:

![Prévia da Aplicação](img/AutoAI.png)

## 🚀 Aplicação Online

A versão de produção desta aplicação está hospedada no Hugging Face Spaces e pode ser acessada diretamente pelo link abaixo:

**[➡️ Acessar a Aplicação Online](https://huggingface.co/spaces/FranciscoMatheus/autoai-email-classifier)**

## Funcionalidades Chave

- **Classificação Inteligente:** Utiliza um modelo de `zero-shot classification` da Hugging Face para categorizar e-mails sem a necessidade de treinamento prévio com dados específicos do domínio.
- **Sugestão de Respostas:** Utiliza um modelo de geração de texto para fornecer respostas contextuais baseadas na categoria identificada pela IA.
- **Interface Amigável:** Design responsivo e intuitivo, permitindo a inserção de e-mails via digitação de texto ou upload de arquivo `.txt`.
- **Feedback Visual:** Animações e indicadores visuais durante o processamento da IA para uma melhor experiência do usuário.
- **Design Robusto:** Layout profissional com uma interface limpa e organizada.
- **Medidas de Segurança:**
    - **Rate Limiting:** Proteção contra abuso na API de classificação, limitando o número de requisições por IP.
    - **HTTPS Automático:** Garantido pela plataforma Hugging Face Spaces.
    - **Servidor de Produção (Gunicorn):** Uso de um servidor WSGI seguro e robusto para o deploy.
    - **Execução como non-root:** O contêiner Docker é executado com um usuário de privilégios limitados para maior segurança.

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando um conjunto de tecnologias modernas para backend, frontend e deploy:

| Categoria | Tecnologia |
|-----------|------------|
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) |
| **Inteligência Artificial** | ![Hugging Face](https://img.shields.io/badge/🤗%20Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![Bulma](https://img.shields.io/badge/Bulma-00D1B2?style=for-the-badge&logo=bulma&logoColor=white) |
| **Infraestrutura & Deploy** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white) |

## 💡 Desafios e Aprendizados

O desenvolvimento deste projeto foi uma jornada prática de resolução de problemas, especialmente na fase de deploy, que simulou desafios comuns em ambientes de produção.

* **Desafio Inicial: Limitação de Recursos na Nuvem**
    * A primeira tentativa de deploy foi em uma plataforma PaaS convencional (Render.com). No entanto, a aplicação falhou repetidamente devido ao limite de 512MB de RAM do plano gratuito, que se mostrou insuficiente para carregar os modelos de linguagem da biblioteca `transformers`.

* **Solução Estratégica: Containerização e Migração**
    * Para superar a limitação de memória, a estratégia foi pivotada. A aplicação foi **containerizada com Docker**, criando um ambiente de execução portátil e consistente.
    * O deploy foi migrado para o **Hugging Face Spaces**, uma plataforma otimizada para aplicações de IA que oferece recursos de hardware mais robustos no plano gratuito, incluindo 16GB de RAM.

* **Aprendizados no Processo de Deploy:**
    * **Gerenciamento Fino de Dependências:** Foi necessário realizar um ajuste detalhado no arquivo `requirements.txt` para garantir a compatibilidade de todas as bibliotecas com o ambiente Python 3.9 do contêiner.
    * **Depuração de Permissões em Docker:** Surgiram desafios complexos de permissão de escrita (`PermissionError`) dentro do contêiner, relacionados ao cache dos modelos de IA. A solução envolveu a reestruturação do `Dockerfile` para gerenciar corretamente as permissões de diretórios.
    * **Infraestrutura como Código:** O uso do `Dockerfile` reforçou a importância de definir a infraestrutura da aplicação como código, garantindo que o ambiente de produção seja replicável e confiável.

Este processo não apenas resultou em uma aplicação funcional, mas também demonstrou a capacidade de diagnosticar problemas de infraestrutura, adaptar a estratégia de tecnologia e implementar soluções robustas para garantir o sucesso do deploy.


## Como Rodar o Projeto Localmente

Siga estes passos para configurar e executar a aplicação em sua máquina local:

### Pré-requisitos

- Python 3.9+ instalado
- Docker instalado (recomendado para replicar o ambiente de produção)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://huggingface.co/spaces/FranciscoMatheus/autoai-email-classifier](https://huggingface.co/spaces/FranciscoMatheus/autoai-email-classifier)
    cd autoai-email-classifier
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

### Executando a Aplicação (Modo Desenvolvimento)

1.  Com o ambiente virtual ativado, execute o servidor Flask:
    ```bash
    python app.py
    ```

2.  Abra seu navegador e acesse: `http://127.0.0.1:5000/`

### Executando com Docker (Modo Produção)

1.  Construa a imagem Docker:
    ```bash
    docker build -t autoai-app .
    ```

2.  Execute o contêiner:
    ```bash
    docker run -p 8000:8000 autoai-app
    ```
3.  Abra seu navegador e acesse: `http://127.0.0.1:8000/`

## Deploy na Nuvem (Hugging Face Spaces)

A aplicação está configurada para deploy automático no Hugging Face Spaces através de:

- `Dockerfile`: Define o ambiente completo, dependências e comando de execução, garantindo consistência entre desenvolvimento e produção.
- `README.md` (este arquivo): Contém a configuração do SDK e da porta para o Hugging Face Spaces.

---

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para abrir uma *issue* ou um *pull request*.