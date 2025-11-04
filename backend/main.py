# main.py - ARQUITETURA FINAL (ASYNC/AWAIT + THREADPOOL CORRIGIDO)

from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import time
import traceback
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from langchain_litellm import ChatLiteLLM
from starlette.concurrency import run_in_threadpool # Importação correta

app = FastAPI()

last_request_time = 0
MIN_INTERVAL = 60

@app.get("/")
def read_root():
    return {"message": "API funcionando!", "version": "3.0.0"}

# 1. Endpoint 'async def' (Correto)
@app.post("/analyze-stock")
async def analyze_stock(request: Request):
    global last_request_time
    
    time_since_last = time.time() - last_request_time
    if time_since_last < MIN_INTERVAL:
        wait_time = MIN_INTERVAL - time_since_last
        raise HTTPException(
            status_code=429,
            detail={
                "message": f"Aguarde {wait_time:.0f} segundos.",
                "wait_seconds": int(wait_time)
            }
        )
    
    # 2. 'await' para ler o JSON (Correto)
    data = await request.json() 
    stock_symbol = data.get('stock_symbol')

    if not stock_symbol:
        raise HTTPException(status_code=400, detail="Campo obrigatório")

    try:
        # 3. Define a função síncrona (bloqueante)
        def run_crew_analysis():
            load_dotenv(override=True) 
            
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY não encontrada")
            
            llm = ChatLiteLLM(
                model="gemini/gemini-2.5-flash",
                temperature=0.7
            )

            search_tool = SerperDevTool(num_results=3)

            # --- CRIAÇÃO DOS AGENTES ---
            julia_agent = Agent(
                role='Analista de Dados Financeiros',
                goal=f'Coletar cotação e dados de {stock_symbol}',
                backstory='Analista financeira especializada.',
                tools=[search_tool],
                llm=llm
            )
            pedro_agent = Agent(
                role='Analista de Sentimento',
                goal=f'Avaliar sentimento sobre {stock_symbol}',
                backstory='Especialista em análise de notícias.',
                tools=[search_tool],
                llm=llm
            )
            key_agent = Agent(
                role='Redator Financeiro',
                goal=f'Escrever relatório sobre {stock_symbol}',
                backstory='Jornalista financeiro experiente.',
                llm=llm
            )

            # --- DEFINIÇÃO DAS TAREFAS ---
            task_julia = Task(
                description=f'Busque e informe a cotação atual, receita e lucro líquido de {stock_symbol}',
                agent=julia_agent,
                expected_output='Resumo de dados financeiros'
            )
            task_pedro = Task(
                description=f'Busque notícias recentes sobre {stock_symbol} e classifique o sentimento (positivo/negativo/neutro)',
                agent=pedro_agent,
                expected_output='Relatório de sentimento',
                context=[task_julia]
            )
            task_key = Task(
                description=f'''
                Com base nos DADOS FINANCEIROS (Tarefa 1) e na ANÁLISE DE SENTIMENTO (Tarefa 2),
                escreva um relatório profissional sobre {stock_symbol} com:
                1. Resumo dos dados
                2. Análise do sentimento
                3. Recomendação: COMPRAR, VENDER ou MANTER
                ''',
                agent=key_agent,
                expected_output='Relatório estruturado',
                context=[task_julia, task_pedro]
            )

            # --- CRIAÇÃO DO CREW ÚNICO ---
            stock_crew = Crew(
                agents=[julia_agent, pedro_agent, key_agent],
                tasks=[task_julia, task_pedro, task_key],
                process=Process.sequential,
                memory=False
            )
            
            resultado_final = stock_crew.kickoff()

            # Extrai os resultados individuais (Corrigido para .raw)
            resultado_julia = task_julia.output.raw if task_julia.output else "Dados de Júlia não coletados."
            resultado_pedro = task_pedro.output.raw if task_pedro.output else "Sentimento de Pedro não analisado."

            # 4. CORREÇÃO: O 'return' deve estar DENTRO da função síncrona
            return {
                "message": str(resultado_final) if resultado_final else "Análise não concluída",
                "dados": str(resultado_julia),
                "sentimento": str(resultado_pedro),
                "status": "success"
            }

        # 5. CORREÇÃO: Executa a função síncrona no threadpool
        result_data = await run_in_threadpool(run_crew_analysis)
        
        # Atualiza o tempo DEPOIS que a tarefa terminar
        last_request_time = time.time()
        
        # 6. CORREÇÃO: Retorna o resultado da função
        return result_data

    except Exception as e:
        error_message = str(e)
        print(f"ERRO: {error_message}")
        traceback.print_exc()
        
        if "rate_limit" in error_message.lower() or "quota" in error_message.lower():
             raise HTTPException(status_code=429, detail={"message": "Limite atingido. Aguarde 60 segundos.", "wait_seconds": 60})
        
        raise HTTPException(status_code=500, detail=f"ERRO INTERNO: {error_message}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)