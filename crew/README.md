## Core concept:
- Agent: an autonomous unit, with an LLM, a role, a goal, a backstory, memory, tools
- Task: a specific assignment to be carried out, with a descriptiong, expected output and agent
- Crew: a team of Agents and Tasks
    - Sequential: run tasks in order 
    - Hierarchical: use a Manager LLM to assign to agents

### YAML Configuration

Agents and Tasks can be created by code, setting the backstory, description, expected ouput, etc... Or you can define each in a YAML file that's provided when you create the code:
```yaml
researcher:
    role: >
        Senior Financial Researcher
    goal: > 
        Research companies, news and potential
    backstory: >
        You are a senior financial researcher, with a talent for finding the most relevant information
    llm: openai/gpt-4o-mini
```

Code:
```python
agent = Agent(config=self.agents_config['researcher'])
```

### `crew.py`

It all comes together with a Crew definition:

```python
@CrewBase
class MyCrew():
    @agent
    def my_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['my_agent']
        )
    
    @task
    def my_task(self) -> Task:
        return Task(
            config=self.tasks_config['my_task']
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

### LLMs

CrewAI uses the super-simple LiteLLM under the hood to interface with almost any LLM:

```python
llm = LLM(model='openai/gpt-4o-mini')
llm = LLM(model='anthropic/claude-3-5-sonnet-latest')
llm = LLM(model='google/gemini-2.0-flash')
llm = LLM(model='groq/llama-3.3-70b-b-versatile')
llm = LLM(
    model='ollama/llama3.2',
    base_url='http://localhost:11434'
)
llm = LLM(
    model='openrouter/deepseek/deepseek-r1',
    base_url='https://api.deepseek.com/v1',
    api_key=os.getenv('OPENROUTER_API_KEY')
)
```

### UV projects

[Installation guile](https://docs.crewai.com/installation)

CrewAI is already installed: `uv tool install crewai`

Create a new project: `crewai create crew my_crew`

This create an entire directory structure:
```
my_crew/
└── src/
    └── my_crew/
        ├── config/
        │   ├── agents.yaml
        │   └── tasks.yaml
        ├── crew.py
        └── main.py 
```

Run: `crewai run`

### Five steps:

1. Create the project: `crewai create crew my_project`
2. Fill in the config yaml files to define the Agents and Tasks
3. Complete the `crew.py` module to create the Agents, Tasks and Crew, referencing the config
4. Update the `main.py` to set config and run
5. Run: `crewai run`

---

### Tools & Context

- Tools: equiping agents with capabilities
- Context: information passed from 1 task to another
