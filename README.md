# 📈 Stock Insider AI (Analista Financeiro com IA)

Um sistema de análise de ações com curadoria humana, orquestrado por um time de agentes de IA (crewAI) e construído em uma arquitetura de microsserviços robusta com Laravel e Python (FastAPI).

> **Status do Projeto:** 🏆 **Versão 3.1 (Arquitetura de Serviços)** - Funcional e Estável.

-----

## 🎯 Visão Geral do Projeto

O objetivo é democratizar análises financeiras de alta qualidade. Diferente de bots comuns, este sistema implementa o conceito de **Human-in-the-loop**: a IA faz o trabalho pesado de coleta e redação, mas um humano (você) tem a palavra final antes da publicação.

### Funcionalidades Principais
* **🤖 Coleta Autônoma:** Agentes de IA varrem a web em busca de dados financeiros e notícias.
* **⚖️ Painel de Curadoria:** Interface administrativa para revisar, editar e aprovar os relatórios gerados.
* **🌎 Portal de Investidores:** Área pública onde visitantes podem ler apenas as análises auditadas e aprovadas.

-----

## 🖥️ Fluxos de Uso da Aplicação (Laravel)

A aplicação principal é construída em **Laravel + Inertia.js**, oferecendo uma experiência de App Nativo (SPA).

### 1. Fluxo do Analista (Admin)
1.  **Login Seguro:** Acesso restrito via autenticação Laravel.
2.  **Solicitação de Análise:** O usuário digita o ticker (ex: `PETR4`, `AAPL`) no Dashboard.
3.  **Processamento:** O Laravel aciona o microsserviço Python e aguarda a resposta.
4.  **Revisão (Curadoria):** O relatório gerado entra como "Rascunho". O analista pode:
    * Editar o texto (Markdown).
    * Corrigir dados.
    * **Aprovar e Publicar**.

### 2. Fluxo do Visitante (Público)
1.  **Navegação:** Acesso à lista de relatórios públicos.
2.  **Leitura:** Visualização de relatórios com formatação profissional, gráficos (se houver) e indicadores, **somente dos itens aprovados**.

-----

## 🏗️ Arquitetura de Microsserviços

O sistema segue o padrão de **Service-Oriented Architecture (SOA)**. O frontend não acessa a IA diretamente; eles conversam via API interna isolada na rede Docker.

### 1. Core Application (Laravel 10)
* **Responsabilidade:** Gestão de usuários, banco de dados MySQL, regras de negócio (aprovação/rejeição) e renderização frontend (Vue 3).
* **Tecnologias:** Laravel Breeze (Auth), Eloquent ORM, Inertia.js.

### 2. AI Intelligence Service (Python FastAPI)
* **Responsabilidade:** Motor de processamento isolado que roda os agentes.
* **Estrutura:**
    * `main.py`: Gateway da API.
    * `schemas.py`: Validação rigorosa de dados com Pydantic.
    * `crew_service.py`: Orquestração dos agentes CrewAI.
* **Tecnologias:** CrewAI, LiteLLM, Google Gemini Pro.

### 🗣️ Protocolo de Comunicação

O Laravel envia requisições HTTP para o container Python:

**Rota:** `POST http://python:8000/analyze-stock`

```php
// Exemplo no Laravel (AnalysisController.php)
$response = Http::timeout(300)->post('http://python:8000/analyze-stock', [
    'symbol' => $ticker // Ex: 'NVDA'
]);
````

-----

## 🤖 O Time de Agentes (CrewAI)

O "cérebro" é composto por três personas técnicas:

1.  **🕵️‍♀️ Júlia (Lead Data Analyst):** Focada em *Hard Data*. Busca P/L, ROE, Cotação e Dividendos no Google.
2.  **🧠 Pedro (Sentiment Specialist):** Focado em *Behavioral Finance*. Lê notícias e define se o mercado está com "Medo" ou "Ganância".
3.  **✍️ Key (Financial Editor):** Editor-Chefe. Recebe os dados dos outros dois e escreve o artigo final em Markdown, já sugerindo a recomendação (Compra/Venda).

-----

## 🚀 Tech Stack

| Categoria | Tecnologia | Detalhe Técnico |
| :--- | :--- | :--- |
| **Backend Core** | **Laravel 10** | PHP 8.2+, Eloquent, Http Client |
| **Frontend** | **Vue.js 3** | Composition API, Inertia.js |
| **Estilização** | **TailwindCSS** | Design responsivo e Tipografia |
| **Microsserviço IA** | **Python 3.11** | FastAPI, Uvicorn |
| **IA Engine** | **Google Gemini** | Modelo `gemini-flash` via LiteLLM |
| **Infraestrutura** | **Docker Compose** | Redes internas, Volumes e Builds |

-----

## ⚙️ Instalação e Execução

### 1\. Configuração Inicial

```bash
git clone [https://github.com/seu-usuario/analista-financeiro-ia.git](https://github.com/seu-usuario/analista-financeiro-ia.git)
cd analista-financeiro-ia
cp .env.example .env
```

**Configure no .env:** `GOOGLE_API_KEY` e `SERPER_API_KEY`.

### 2\. Build e Deploy (Docker)

```bash
docker-compose up -d --build
```

### 3\. Instalação de Dependências

```bash
# Instalar dependências do Laravel e Vue
docker-compose exec laravel_app composer install
docker-compose exec laravel_app npm install
docker-compose exec laravel_app npm run build

# Criar tabelas no banco
docker-compose exec laravel_app php artisan migrate
```

### 4\. Acesso

  * **Aplicação:** [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  * **API Docs:** [http://localhost:8001/docs](https://www.google.com/search?q=http://localhost:8001/docs)
