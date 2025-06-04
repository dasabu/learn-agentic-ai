from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from stock_picker.tools.push_tool import PushNotificationTool

# Define schemas for agent structured output
class TrendingCompany(BaseModel):
    """A company that is in the news and attracting attention"""
    name: str = Field(description="The name of the company")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """List of multiple trending companies that are in the news"""
    companies: List[TrendingCompany] = Field(description="List of trending companies in the news")

class TrendingCompanyResearch(BaseModel):
    """Detailed research on a company"""
    name: str = Field(description="The name of the company")
    market_position: str = Field(description="Current market position and competitive analysis of the company")
    future_outlook: str = Field(description="Future outlook and growth prospects of the company")
    investment_potential: str = Field(description="Investment potential and suitability for investment of the company")    

class TrendingCompanyResearchList(BaseModel):
    """A list of detailed research on all the companies"""
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")

@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents: 'config/agents.yaml'
    tasks: 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_company_finder'],
            tools=[SerperDevTool()]
        )
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_researcher'],
            tools=[SerperDevTool()]
        )
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_picker'],
            tools=[PushNotificationTool()] # Custom Tool
        )
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList # Structured Output
        )
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList # Structured Output
        )
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company']
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the (Manager) StockPicker crew"""
        manager_agent = Agent(
            config = self.agents_config['manager'],
            allow_delegation=True # Handoff in OpenAI Agent SDK
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical, # Must define a manager agent to use hierarchical process
            verbose=True,
            manager_agent=manager_agent,
            # Not necessary to define a specific manager agent, can do as below:
            # manager_llm='openai/gpt-4o'
        )
