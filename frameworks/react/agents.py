"""React framework agents."""
from typing import List
from crewai import Agent
from frameworks.base import BaseAgents


class ReactAgents(BaseAgents):
    """Factory for React-specific agents."""
    
    @property
    def framework_name(self) -> str:
        return "React"
    
    def react_architect(self, tools: List) -> Agent:
        return self.create_architect(
            tools=tools,
            backstory="""\
                Senior React architect with expertise in modern React development,
                hooks, context API, Redux, and component architecture. You design
                scalable and maintainable React applications.""",
            goal="Design React component architecture and structure for requirements",
        )
    
    def react_programmer(self, tools: List) -> Agent:
        return self.create_programmer(
            tools=tools,
            backstory="""\
                Expert React developer with experience in JSX, ES6+, component
                lifecycle, state management, and the React ecosystem. You write
                clean, efficient, and testable React code.""",
            goal="Implement React components according to architecture design",
        )
    
    def react_tester(self, tools: List) -> Agent:
        return self.create_tester(
            tools=tools,
            backstory="""\
                React testing expert specializing in Jest, React Testing Library,
                and Cypress. You ensure comprehensive test coverage for components,
                hooks, and user interactions.""",
            goal="Write comprehensive tests for React components",
        )
    
    def react_reviewer(self, tools: List) -> Agent:
        return self.create_reviewer(
            tools=tools,
            backstory="""\
                Senior React engineer focused on code quality, performance,
                accessibility, and best practices. You ensure code follows
                React conventions and maintains high standards.""",
            goal="Review React code for quality and best practices",
        )
