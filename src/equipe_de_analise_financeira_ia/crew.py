import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperScrapeWebsiteTool,
	SerperDevTool
)

import g





@CrewBase
class EquipeDeAnaliseFinanceiraIaCrew:
    """EquipeDeAnaliseFinanceiraIa crew"""

    
    @agent
    def julia___analista_de_dados_financeiros(self) -> Agent:

        
        return Agent(
            config=self.agents_config["julia___analista_de_dados_financeiros"],
            
            
            tools=[
				SerperScrapeWebsiteTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def pedro___analista_de_sentimento_de_mercado(self) -> Agent:

        
        return Agent(
            config=self.agents_config["pedro___analista_de_sentimento_de_mercado"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def key___jornalista_financeiro_senior(self) -> Agent:

        
        return Agent(
            config=self.agents_config["key___jornalista_financeiro_senior"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def coleta_de_dados_financeiros(self) -> Task:
        return Task(
            config=self.tasks_config["coleta_de_dados_financeiros"],
            markdown=False,
            
            
        )
    
    @task
    def analise_de_sentimento_de_mercado(self) -> Task:
        return Task(
            config=self.tasks_config["analise_de_sentimento_de_mercado"],
            markdown=False,
            
            
        )
    
    @task
    def redacao_do_artigo_final(self) -> Task:
        return Task(
            config=self.tasks_config["redacao_do_artigo_final"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the EquipeDeAnaliseFinanceiraIa crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
