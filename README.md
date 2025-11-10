# 📈 Analista Financeiro com IA

Um sistema de análise de ações com curadoria humana, alimentado por um time de agentes de IA (crewAI) e construído em uma arquitetura de microsserviços com Laravel e Python (FastAPI).

> **Status do Projeto:** 🏆 **Produto Mínimo Viável (MVP) 100% Concluído e Funcional.**

-----

## 🎯 Principais Funcionalidades

  * **🤖 Análise de IA Multi-Agente:** Utiliza um time de IAs, cada uma com uma especialidade, para coletar dados, analisar sentimentos e redigir o relatório.
  * **🧑‍⚖️ Fluxo de Curadoria Humana:** Garante que nenhum relatório seja publicado sem que um "Fator Humano" revise, edite e aprove o conteúdo.
  * **🌎 Portal Público:** Visitantes podem acessar uma lista pública de *apenas* relatórios aprovados, com formatação limpa e profissional.

-----

## 🏗️ Arquitetura de Microsserviços

O projeto não é um monolito. Ele é dividido em dois "cérebros" independentes que se comunicam via API interna, garantindo estabilidade e isolamento.

### 1\. Frontend & API Principal (A Casa)

  * **Tecnologia:** Laravel (PHP) + Inertia.js + Vue.js
  * **Responsabilidades:**
      * Servir o frontend (páginas `.vue`).
      * Gerenciar segurança (login, middleware, autenticação).
      * Controlar o "Fator Humano" (Painel de Curadoria).
      * Conectar-se ao banco de dados (MySQL).

### 2\. Backend & IA (A Edícula da IA)

  * **Tecnologia:** Python + FastAPI
  * **Responsabilidades:**
      * Servir como um servidor de API de IA independente.
      * Orquestrar os agentes de IA (crewAI).
      * Executar a análise e devolver o relatório em Markdown.

### 🗣️ Comunicação

A comunicação é limpa e direta. O Laravel (cliente) chama o FastAPI (servidor):

```php
// Em App/Http/Controllers/AnalysisController.php
Http::post('http://python:8000/generate_report', [
    'ticker' => $request->ticker
]);
```

-----

## 🤖 O Time de Agentes (crewAI)

O cérebro da IA é composto por três agentes especializados que colaboram para criar o relatório:

  * **Júlia (Analista Quantitativa):** Coleta os dados "frios" (P/L, ROE, Receita) usando ferramentas de busca.
  * **Pedro (Analista Qualitativo):** Coleta o sentimento "quente" do mercado e as notícias recentes (Bullish/Bearish).
  * **Key (Redator-Chefe):** Combina os dados de Júlia e Pedro para redigir um relatório final coeso em Markdown.

-----

## 🚀 Tecnologias Utilizadas

| Categoria | Tecnologia | Propósito |
| :--- | :--- | :--- |
| **Frontend & API Principal** | **Laravel (PHP)** | Backend principal, rotas, auth, DB |
| | **Inertia.js + Vue.js** | Frontend reativo (SPA) |
| | **TailwindCSS** | Estilização da UI |
| | **@tailwindcss/typography** | Renderização "bonita" do Markdown |
| **Serviço de IA** | **Python** | Linguagem do microsserviço |
| | **FastAPI** | Servidor de API de alta performance |
| **Framework de IA** | **crewAI** | Orquestração dos agentes de IA |
| | **Google Gemini** | Modelo de IA para geração de texto |
| | **SerperDevTool** | Ferramenta de busca para os agentes |
| **Infraestrutura** | **Docker & Docker Compose**| Ambiente de desenvolvimento e microsserviços |
| **Banco de Dados** | **MySQL** | Armazenamento dos relatórios e usuários |

-----

## 🔄 Como Usar a Aplicação (Fluxos de Usuário)

Existem dois fluxos principais na plataforma: o do **Admin (Fator Humano)** e o do **Visitante**.

#### 1\. Fluxo do Admin (Curadoria)

1.  **Login:** Acesse `/login` e autentique-se.
2.  **Gerar Análise:** Navegue até a página "Análise".
3.  **Solicitar Relatório:** Digite o ticker da ação (ex: `GOOGL`, `AAPL`) e clique em "Gerar".
4.  **Aguardar a IA:** O sistema irá processar e salvar um rascunho no banco com status `pending_review`.
5.  **Revisar:** Navegue até o "Painel de Curadoria". O novo relatório aparecerá na lista.
6.  **Editar:** Clique em "Revisar". Edite o texto gerado pela IA, faça correções e adicione suas notas.
7.  **Publicar:** Clique em "Aprovar e Publicar". O relatório mudará seu status para `approved` e sairá desta lista.

#### 2\. Fluxo do Visitante (Público)

1.  **Acessar:** Acesse a página inicial (ex: `http://localhost:8000`).
2.  **Navegar:** Clique no link "Relatórios" no menu superior.
3.  **Visualizar:** O visitante verá uma lista de *todos* os relatórios que foram **aprovados** pelo Fator Humano.
4.  **Ler:** Clicando em um relatório, ele pode ler a análise completa, renderizada de forma limpa e profissional.

-----

## ⚙️ Como Executar Localmente (Instalação)

Siga estes passos para configurar o ambiente de desenvolvimento em sua máquina.

### Pré-requisitos

  * [Git](https://git-scm.com/)
  * [Docker](https://www.docker.com/products/docker-desktop/)
  * [Docker Compose](https://docs.docker.com/compose/) (geralmente incluído no Docker Desktop)

### 1\. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2\. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo. Você **precisará** editar este novo arquivo `.env`.

```bash
cp .env.example .env
```

Dentro do arquivo `.env`:

  * Assegure-se de que `DB_HOST=db` (para apontar para o container do Docker).
  * Adicione suas chaves de API (`SERPER_API_KEY`, `GOOGLE_API_KEY`).

### 3\. Subir os Containers

Este comando vai construir e iniciar todos os serviços (Laravel, Python, Nginx, MySQL).

```bash
docker-compose up -d --build
```

### 4\. Instalar Dependências (Backend & Frontend)

Execute os seguintes comandos para instalar as dependências do Composer e NPM e preparar o banco de dados.

```bash
# 1. Instalar dependências do PHP
docker-compose exec laravel_app composer install

# 2. Gerar a chave da aplicação Laravel
docker-compose exec laravel_app php artisan key:generate

# 3. Rodar as migrações do banco de dados (criar as tabelas)
docker-compose exec laravel_app php artisan migrate

# 4. Instalar dependências do JavaScript
docker-compose exec laravel_app npm install
```

### 5\. Rodar o Ambiente de Desenvolvimento

Para compilar os assets do frontend e ativar o "hot reload" (que atualiza o site automaticamente quando você muda o código):

```bash
docker-compose exec laravel_app npm run dev
```

*(Se você quiser apenas "compilar" para produção, use `npm run build`)*

### 6\. Acessar o Projeto

Pronto\! O projeto está rodando:

  * **Site (Laravel):** [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
  * **API de IA (FastAPI Docs):** [http://localhost:8001/docs](https://www.google.com/search?q=http://localhost:8001/docs)
