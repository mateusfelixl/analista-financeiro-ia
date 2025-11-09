# 📈 Analista Financeiro com IA

Um sistema de análise de ações com curadoria humana, alimentado por um time de agentes de IA (crewAI) e construído em uma arquitetura de microsserviços com Laravel e Python (FastAPI).

![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)
![Laravel](https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)

> **Status do Projeto:** 🏆 **Produto Mínimo Viável (MVP) 100% Concluído e Funcional.**

---

## 🎯 Principais Funcionalidades

* **🤖 Análise de IA Multi-Agente:** Utiliza um time de IAs, cada uma com uma especialidade, para coletar dados, analisar sentimentos e redigir o relatório.
* **🧑‍⚖️ Fluxo de Curadoria Humana:** Garante que nenhum relatório seja publicado sem que um "Fator Humano" revise, edite e aprove o conteúdo.
* **🌎 Portal Público:** Visitantes podem acessar uma lista pública de *apenas* relatórios aprovados, com formatação limpa e profissional.

---

## 🏗️ Arquitetura de Microsserviços

O projeto não é um monolito. Ele é dividido em dois "cérebros" independentes que se comunicam via API interna, garantindo estabilidade e isolamento.

### 1. Frontend & API Principal (A Casa)
* **Tecnologia:** Laravel (PHP) + Inertia.js + Vue.js
* **Responsabilidades:**
    * Servir o frontend (páginas `.vue`).
    * Gerenciar segurança (login, middleware, autenticação).
    * Controlar o "Fator Humano" (Painel de Curadoria).
    * Conectar-se ao banco de dados (MySQL).

### 2. Backend & IA (A Edícula da IA)
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

🤖 O Time de Agentes (crewAI)
O cérebro da IA é composto por três agentes especializados que colaboram para criar o relatório:
 * Júlia (Analista Quantitativa): Coleta os dados "frios" (P/L, ROE, Receita) usando ferramentas de busca.
 * Pedro (Analista Qualitativo): Coleta o sentimento "quente" do mercado e as notícias recentes (Bullish/Bearish).
 * Key (Redator-Chefe): Combina os dados de Júlia e Pedro para redigir um relatório final coeso em Markdown.
🚀 Tecnologias Utilizadas
| Categoria | Tecnologia | Propósito |
|---|---|---|
| Frontend & API Principal | Laravel (PHP) | Backend principal, rotas, auth, DB |
|  | Inertia.js + Vue.js | Frontend reativo (SPA) |
|  | TailwindCSS | Estilização da UI |
|  | @tailwindcss/typography | Renderização "bonita" do Markdown |
| Serviço de IA | Python | Linguagem do microsserviço |
|  | FastAPI | Servidor de API de alta performance |
| Framework de IA | crewAI | Orquestração dos agentes de IA |
|  | Google Gemini | Modelo de IA para geração de texto |
|  | SerperDevTool | Ferramenta de busca para os agentes |
| Infraestrutura | Docker & Docker Compose | Ambiente de desenvolvimento e microsserviços |
| Banco de Dados | MySQL | Armazenamento dos relatórios e usuários |

🔄 Como Usar a Aplicação (Fluxos de Usuário)
Existem dois fluxos principais na plataforma: o do Admin (Fator Humano) e o do Visitante.
1. Fluxo do Admin (Curadoria)
 * Login: Acesse /login e autentique-se.
 * Gerar Análise: Navegue até a página "Análise".
 * Solicitar Relatório: Digite o ticker da ação (ex: GOOGL, AAPL) e clique em "Gerar".
 * Aguardar a IA: O sistema irá processar e salvar um rascunho no banco com status pending_review.
 * Revisar: Navegue até o "Painel de Curadoria". O novo relatório aparecerá na lista.
 * Editar: Clique em "Revisar". Edite o texto gerado pela IA, faça correções e adicione suas notas.
 * Publicar: Clique em "Aprovar e Publicar". O relatório mudará seu status para approved e sairá desta lista.
2. Fluxo do Visitante (Público)
 * Acessar: Acesse a página inicial (ex: http://localhost:8000).
 * Navegar: Clique no link "Relatórios" no menu superior.
 * Visualizar: O visitante verá uma lista de todos os relatórios que foram aprovados pelo Fator Humano.
 * Ler: Clicando em um relatório, ele pode ler a análise completa, renderizada de forma limpa e profissional.

⚙️ Como Executar Localmente (Instalação)
 * Clonar o repositório:
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio

 * Configurar Variáveis de Ambiente:
   * Copie .env.example para .env.
   * No .env, configure o DB_HOST=db-data.
   * Adicione suas chaves de API (SERPER_API_KEY, GEMINI_API_KEY) no .env.
 * Subir os Containers:
   docker-compose up -d --build

 * Instalar Dependências e Migrar (Laravel):
   docker-compose exec laravel_app composer install
docker-compose exec laravel_app php artisan migrate
docker-compose exec laravel_app php artisan key:generate

 * Instalar Dependências (Frontend):
   docker-compose exec laravel_app npm install
docker-compose exec laravel_app npm run build

 * Acessar o Projeto:
   * Frontend (Laravel): http://localhost:8000
   * API de IA (FastAPI Docs): http://localhost:8081/docs
<!-- end list -->
