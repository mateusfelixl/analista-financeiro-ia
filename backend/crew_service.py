import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_litellm import ChatLiteLLM
from config import Config

class FinancialAnalysisService:
    
    def __init__(self):
        
        if Config.GOOGLE_API_KEY:
            os.environ["GEMINI_API_KEY"] = Config.GOOGLE_API_KEY

        
        self.llm = ChatLiteLLM(
            model=Config.GEMINI_MODEL, 
            temperature=0.7,
            verbose=True
        )

        self.search_tool = SerperDevTool(n_results=5)

    def execute_analysis(self, stock_symbol: str) -> dict:
        # --- AGENTES ---
        
        analyst_data = Agent(
            role='Senior Financial Data Analyst',
            name='Júlia',
            goal=f'Extrair indicadores fundamentais de {stock_symbol}',
            backstory="Analista quantitativa sênior focado em números e dados do mercado.",
            tools=[self.search_tool],
            llm=self.llm,
            allow_delegation=False
        )

        analyst_sentiment = Agent(
            role='Market Sentiment Specialist',
            name='Pedro',
            goal=f'Mapear sentimento sobre {stock_symbol}',
            backstory="Especialista em finanças comportamentais e notícias de mercado.",
            tools=[self.search_tool],
            llm=self.llm,
            allow_delegation=False
        )

        editor_chief = Agent(
            role='Financial Journalist',
            name='Key',
            goal=f'Escrever relatório final sobre {stock_symbol}',
            backstory="Jornalista que consolida dados e define recomendação.",
            llm=self.llm,
            allow_delegation=False
        )

        # --- TAREFAS ---
        
        task_data = Task(
            description=f'Pesquise preço atual, P/L e notícias de {stock_symbol}.',
            agent=analyst_data,
            expected_output='Dados financeiros brutos.'
        )

        task_sentiment = Task(
            description=f'Analise o sentimento das notícias sobre {stock_symbol} (Positivo/Negativo).',
            agent=analyst_sentiment,
            expected_output='Análise de sentimento.',
            context=[task_data]
        )

        task_report = Task(
            description=f'Escreva um relatório final sobre {stock_symbol} iniciando com "# Relatório".',
            agent=editor_chief,
            expected_output='Relatório em Markdown.',
            context=[task_data, task_sentiment]
        )

        # --- EXECUÇÃO ---
        crew = Crew(
            agents=[analyst_data, analyst_sentiment, editor_chief],
            tasks=[task_data, task_sentiment, task_report],
            process=Process.sequential,
            verbose=True
        )

        final_result = crew.kickoff()

        return {
            "report": str(final_result),
            "raw_data": str(task_data.output.raw) if task_data.output else "N/A",
            "raw_sentiment": str(task_sentiment.output.raw) if task_sentiment.output else "N/A"
        }