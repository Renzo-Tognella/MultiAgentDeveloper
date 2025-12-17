"""
Base classes for framework-specific agents and tasks.
Following DRY principle - shared functionality extracted to base classes.
"""
from abc import ABC, abstractmethod
from typing import List, Dict

from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from textwrap import dedent


class BaseAgents(ABC):
    """Base class for framework-specific agent factories."""
    
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7):
        self._llm = ChatOpenAI(model_name=model, temperature=temperature)
    
    @property
    @abstractmethod
    def framework_name(self) -> str:
        """Return the framework name for role descriptions."""
        pass
    
    def create_architect(self, tools: List, backstory: str, goal: str) -> Agent:
        """Create an architect agent."""
        return Agent(
            role=f"{self.framework_name} Architect",
            backstory=dedent(backstory),
            goal=dedent(goal),
            tools=tools,
            allow_delegation=False,
            verbose=False,
            llm=self._llm,
        )
    
    def create_programmer(self, tools: List, backstory: str, goal: str) -> Agent:
        """Create a programmer agent."""
        return Agent(
            role=f"{self.framework_name} Developer",
            backstory=dedent(backstory),
            goal=dedent(goal),
            tools=tools,
            allow_delegation=False,
            verbose=False,
            llm=self._llm,
        )
    
    def create_tester(self, tools: List, backstory: str, goal: str) -> Agent:
        """Create a tester agent."""
        return Agent(
            role=f"{self.framework_name} Testing Specialist",
            backstory=dedent(backstory),
            goal=dedent(goal),
            tools=tools,
            allow_delegation=False,
            verbose=False,
            llm=self._llm,
        )
    
    def create_reviewer(self, tools: List, backstory: str, goal: str) -> Agent:
        """Create a reviewer agent."""
        return Agent(
            role=f"{self.framework_name} Code Reviewer",
            backstory=dedent(backstory),
            goal=dedent(goal),
            tools=tools,
            allow_delegation=False,
            verbose=False,
            llm=self._llm,
        )


class BaseTasks(ABC):
    """Base class for framework-specific task factories."""
    
    INCENTIVE = "Deliver your best work for optimal results."
    
    @property
    @abstractmethod
    def framework_name(self) -> str:
        """Return the framework name for task descriptions."""
        pass
    
    def create_architecture_task(
        self, 
        agent: Agent, 
        analysis: Dict,
        description: str,
        expected_output: str
    ) -> Task:
        """Create an architecture design task."""
        return Task(
            description=self._format_description(description, analysis),
            expected_output=expected_output,
            agent=agent,
        )
    
    def create_implementation_task(
        self,
        agent: Agent,
        context: List[Task],
        description: str,
        expected_output: str
    ) -> Task:
        """Create an implementation task."""
        return Task(
            description=dedent(description),
            expected_output=expected_output,
            agent=agent,
            context=context,
        )
    
    def create_testing_task(
        self,
        agent: Agent,
        context: List[Task],
        description: str,
        expected_output: str
    ) -> Task:
        """Create a testing task."""
        return Task(
            description=dedent(description),
            expected_output=expected_output,
            agent=agent,
            context=context,
        )
    
    def create_review_task(
        self,
        agent: Agent,
        context: List[Task],
        description: str,
        expected_output: str
    ) -> Task:
        """Create a code review task."""
        return Task(
            description=dedent(description),
            expected_output=expected_output,
            agent=agent,
            context=context,
        )
    
    def _format_description(self, template: str, analysis: Dict) -> str:
        """Format task description with analysis data."""
        return dedent(template).format(
            requirements=analysis.get("requirements", ""),
            files_to_modify=analysis.get("files_to_modify", []),
            files_to_create=analysis.get("files_to_create", []),
            incentive=self.INCENTIVE,
        )
