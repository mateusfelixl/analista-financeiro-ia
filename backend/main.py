# --- main.py (Servidor da API de Análise Financeira) ---
 

# Importações principais
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import time
import traceback
from dotenv import load_dotenv

# --- 1. IMPORTAÇÃO DA DATA (COM FUSO HORÁRIO) ---
from datetime import datetime
from zoneinfo import ZoneInfo 

# Importações do CrewAI e LLMs
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_litellm import ChatLiteLLM
from starlette.concurrency import run_in_threadpool 

# --- 2. CONFIGURAÇÃO INICIAL DO SERVIDOR ---
load_dotenv(override=True) 
app = FastAPI()

# --- 3. CONTROLE DE RATE LIMIT ---
last_request_time = 0
MIN_INTERVAL = 60 # Intervalo mínimo de 60 segundos entre chamadas

@app.get("/")
def read_root():
    return {"message": "Servidor 'Cérebro' (Python/FastAPI) está online.", "version": "2.3.0"}

@app.post("/analyze-stock")
async def analyze_stock(request: Request):
    global last_request_time
    
    # --- Rate Limit ---
    time_since_last = time.time() - last_request_time
    if time_since_last < MIN_INTERVAL:
        wait_time = MIN_INTERVAL - time_since_last
        raise HTTPException(
            status_code=429,
            detail={
                "message": f"Rate limit atingido. Por favor, aguarde {wait_time:.0f} segundos.",
                "wait_seconds": int(wait_time)
            }
        )
    
    try:
        data = await request.json() 
        stock_symbol = data.get('stock_symbol')

        if not stock_symbol:
            raise HTTPException(status_code=400, detail="O 'stock_symbol' é obrigatório.")

        print(f"\n--- REQUISIÇÃO RECEBIDA: Analisando {stock_symbol} ---")

        # --- A FUNÇÃO SÍNCRONA DO CREW ---
        def run_crew_analysis():
            
            google_api_key = os.getenv("GOOGLE_API_KEY")
            serper_api_key = os.getenv("SERPER_API_KEY")
            if not google_api_key or not serper_api_key:
                raise ValueError("GOOGLE_API_KEY ou SERPER_API_KEY não encontradas no .env")

            # --- Configura o LLM ---
            llm = ChatLiteLLM(
                model="gemini/gemini-2.5-flash",
                temperature=0.5 
            )

            # --- Configura a Ferramenta de Busca ---
            search_tool = SerperDevTool(num_results=4, api_key=serper_api_key) # 4 resultados

            # --- 4. CORREÇÃO DA DATA ---
            try:
                # Pega a data/hora ATUAL no fuso de São Paulo
                fuso_horario_sp = ZoneInfo("America/Sao_Paulo")
                data_atual = datetime.now(fuso_horario_sp).strftime("%d/%m/%Y")
            except Exception:
                # Fallback (caso o 'zoneinfo' falhe, o que é raro)
                data_atual = datetime.now().strftime("%d/%m/%Y")
                print("Aviso: Falha ao carregar fuso 'America/Sao_Paulo'. Usando data UTC.")

            print(f"--- Data formatada para o prompt: {data_atual} ---")

            # --- 1. AGENTE "JÚLIA" (A Quant) ---
            julia_agent = Agent(
                role='Analista Quantitativa Sênior (Quant)',
                goal=f'Extrair dados financeiros frios e brutos para {stock_symbol}, focando em P/L, ROE e receita trimestral.',
                backstory='Uma especialista em dados de Wall Street. Você é cética, odeia "achismos" e só confia em números. Seu trabalho é encontrar os dados financeiros puros.',
                tools=[search_tool],
                llm=llm,
                verbose=True
            )

            # --- 2. AGENTE "PEDRO" (O Investigador) ---
            pedro_agent = Agent(
                role='Investigador de Mídia e Sentimento',
                goal=f'Descobrir o "hype" e o sentimento qualitativo (Bullish ou Bearish) do mercado sobre {stock_symbol}.',
                backstory='Um ex-jornalista investigativo. Você lê nas entrelinhas das notícias, fóruns e redes sociais para descobrir a opinião real dos analistas e do público.',
                tools=[search_tool],
                llm=llm,
                verbose=True
            )

            # --- 3. AGENTE "KEY" (A Redatora-Chefe) ---
            key_agent = Agent(
                role='Redatora-Chefe de Análise Financeira',
                goal=f'Combinar os dados "frios" (Júlia) e "quentes" (Pedro) em um relatório final coeso para {stock_symbol}.',
                backstory='Uma jornalista financeira experiente com 20 anos de casa. Você tem a habilidade de traduzir números complexos e sentimentos de mercado em uma recomendação de investimento clara e justificada.',
                llm=llm,
                verbose=True
            )

            # --- Definição das TAREFAS ---
            task_julia = Task(
                description=f'Busque os seguintes dados para {stock_symbol}: 1. Cotação atual. 2. P/L (Preço/Lucro). 3. ROE (Retorno sobre Patrimônio). 4. Receita do último trimestre. 5. Lucro Líquido do último trimestre.',
                agent=julia_agent,
                expected_output='Um resumo em "bullet points" contendo apenas os dados numéricos solicitados.'
            )
            task_pedro = Task(
                description=f'Analise as 3 notícias mais recentes e o sentimento geral do mercado para {stock_symbol}. O sentimento é Positivo (Bullish), Negativo (Bearish) ou Neutro?',
                agent=pedro_agent,
                expected_output='Um parágrafo resumindo o sentimento geral e as notícias que o causam.',
                context=[task_julia]
            )
            task_key = Task(
                description=f'''
                Use os dados financeiros da Tarefa 1 (Júlia) e a análise de sentimento da Tarefa 2 (Pedro).
                Escreva um relatório profissional em Português (formato Markdown) sobre {stock_symbol}.
                
                O relatório DEVE incluir a data de hoje, que é: {data_atual}

                O relatório DEVE ter esta estrutura:
                1. Um título (ex: # Relatório de Investimento: {stock_symbol})
                2. A data (ex: **Data:** {data_atual})
                3. Uma seção "## Resumo dos Dados" (os números da Júlia).
                4. Uma seção "## Análise de Sentimento" (o "hype" do Pedro).
                5. Uma seção "## Recomendação" (COMPRAR, VENDER ou MANTER) com uma "Justificativa:" clara.
                
                IMPORTANTE: NÃO inclua uma linha de "Editor-Chefe" ou "Autor". O relatório deve ser anônimo.
                ''',
                agent=key_agent,
                expected_output='O relatório final completo em Português, formato Markdown, com a data de hoje.',
                context=[task_julia, task_pedro]
            )

            # --- Montagem e Execução do Crew ---
            stock_crew = Crew(
                agents=[julia_agent, pedro_agent, key_agent],
                tasks=[task_julia, task_pedro, task_key],
                process=Process.sequential,
                memory=False,
                verbose=True 
            )
            
            print(f"--- EXECUTANDO CREW (v2.3) PARA {stock_symbol} ---")
            resultado_final = stock_crew.kickoff()
            print(f"--- EXECUÇÃO CONCLUÍDA ---")

            resultado_julia = task_julia.output.raw if task_julia.output else "Dados de Júlia não coletados."
            resultado_pedro = task_pedro.output.raw if task_pedro.output else "Sentimento de Pedro não analisado."

            return {
                "message": str(resultado_final) if resultado_final else "Análise não concluída.",
                "dados": str(resultado_julia),
                "sentimento": str(resultado_pedro),
                "status": "success"
            }

        # --- Lógica de Execução e Erro ---
        
        result_data = await run_in_threadpool(run_crew_analysis)
        
        last_request_time = time.time()
        
        return result_data

    except Exception as e:
        error_message = str(e)
        print(f"--- 🛑 ERRO CRÍTICO NO main.py 🛑 ---")
        print(f"Erro: {error_message}")
        traceback.print_exc()
        
        if "rate_limit" in error_message.lower() or "quota" in error_message.lower():
             raise HTTPException(status_code=429, detail={"message": "API do Google atingiu o limite de taxa (quota). Aguarde 60 segundos.", "wait_seconds": 60})
        
        raise HTTPException(status_code=500, detail=f"ERRO INTERNO NO PYTHON: {error_message}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)