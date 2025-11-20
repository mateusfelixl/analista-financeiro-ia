# 📈 Stock Insider AI (Analista Financeiro com IA)

Um sistema de análise de ações com curadoria humana, orquestrado por um time de agentes de IA (crewAI) e construído em uma arquitetura de microsserviços robusta com Laravel e Python (FastAPI).

> **Status do Projeto:** 🏆 **Versão 3.1 (Arquitetura de Serviços)** - Funcional e Estável.

-----

## 🎯 Principais Funcionalidades

* **🤖 IA Multi-Agente Autônoma:** Três agentes especializados (Dados, Sentimento e Editorial) colaboram para gerar relatórios financeiros completos.
* **🛡️ Validação Rigorosa:** O backend Python utiliza **Pydantic** para garantir a integridade dos dados antes mesmo de acionar a IA.
* **🧑‍⚖️ Fluxo de Curadoria Humana (Human-in-the-loop):** Nenhum conteúdo vai ao ar sem aprovação. O humano atua como Editor-Chefe final.
* **🌎 Portal Público:** Interface limpa para visitantes consumirem apenas conteúdos verificados.

-----

## 🏗️ Arquitetura de Microsserviços

O sistema segue o padrão de **Service-Oriented Architecture (SOA)**. O frontend não acessa a IA diretamente; eles conversam via API interna isolada na rede Docker.

### 1. Core Application (Laravel 10)
* **Responsabilidade:** Gestão de usuários, banco de dados, painel administrativo e renderização frontend (Inertia.js + Vue 3).
* **Segurança:** Middleware de autenticação e proteção de rotas.

### 2. AI Intelligence Service (Python FastAPI)
* **Responsabilidade:** Motor de processamento isolado.
* **Estrutura:**
    * `main.py`: Gateway da API.
    * `schemas.py`: Contratos de dados (Data Contracts).
    * `crew_service.py`: Lógica de negócios e orquestração dos agentes.
* **Tecnologia:** CrewAI + LiteLLM + Google Gemini.

### 🗣️ Protocolo de Comunicação

O Laravel envia requisições para o serviço Python, que processa em background threads para otimizar o tempo de resposta.

**Rota:** `POST http://python:8000/analyze-stock`

```php
// Exemplo de implementação no AnalysisController.php
$response = Http::timeout(300)->post('http://python:8000/analyze-stock', [
    'symbol' => $ticker // Ex: 'AAPL'
]);

🤖 O Time de Agentes (CrewAI)
O "cérebro" é composto por personas técnicas que utilizam ferramentas de busca (SerperDevTool) em tempo real:

🕵️‍♀️ Júlia (Lead Data Analyst): Especialista em Hard Data. Busca indicadores (P/L, ROE, Cotação) ignorando ruídos.

🧠 Pedro (Sentiment Specialist): Especialista em Behavioral Finance. Analisa o tom das notícias (Medo vs. Ganância).

✍️ Key (Financial Editor): Sintetiza as informações técnicas e comportamentais em um relatório acionável em Markdown.

🚀 Tech Stack

Categoria,Tecnologia,Detalhe Técnico
Backend Core,Laravel 10,"PHP 8.2+, Eloquent ORM"
Frontend,Vue.js 3 + Inertia,Single Page Application (SPA)
AI Service,Python 3.11,"FastAPI, Pydantic"
AI Framework,CrewAI,Orquestração de Agentes Autônomos
LLM Engine,Google Gemini,Modelo gemini-flash via LiteLLM
Infraestrutura,Docker Compose,Orquestração de containers e redes internas

⚙️ Instalação e Execução
Siga estes passos para levantar o ambiente completo via Docker.

1. Configuração Inicial

# Clone o repositório
git clone [https://github.com/seu-usuario/analista-financeiro-ia.git](https://github.com/seu-usuario/analista-financeiro-ia.git)
cd analista-financeiro-ia

# Configure as variáveis de ambiente
cp .env.example .env

Atenção: No arquivo .env, configure suas chaves:

GOOGLE_API_KEY (Para o Gemini)

SERPER_API_KEY (Para as buscas no Google)

2. Build e Deploy Local
Como utilizamos microsserviços, o Docker Compose gerencia tudo (banco, redis, python, php).

# Constrói as imagens e sobe os containers
docker-compose up -d --build

3. Instalação de Dependências (Primeira vez)
Execute estes comandos para configurar o Laravel dentro do container:

# Instalar pacotes PHP e Node
docker-compose exec laravel_app composer install
docker-compose exec laravel_app npm install
docker-compose exec laravel_app npm run build

# Rodar migrações do banco
docker-compose exec laravel_app php artisan migrate

4. Acesso
Painel Principal: http://localhost:8000

API Docs (Swagger): http://localhost:8001/docs
