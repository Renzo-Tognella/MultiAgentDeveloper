"""Ruby on Rails framework agents."""
from typing import List
from crewai import Agent
from frameworks.base import BaseAgents


class RailsAgents(BaseAgents):
    """Factory for Rails-specific agents."""
    
    @property
    def framework_name(self) -> str:
        return "Ruby on Rails"
    
    def rails_architect(self, tools: List) -> Agent:
        return self.create_architect(
            tools=tools,
            backstory="""\
                Senior Rails architect with expertise in MVC architecture,
                RESTful design, Active Record, and Rails conventions. You design
                scalable and maintainable Rails applications.""",
            goal="Design Rails architecture including models, controllers, and routes",
        )
    
    def rails_programmer(self, tools: List) -> Agent:
        return self.create_programmer(
            tools=tools,
            backstory="""\
                Expert Rails developer with experience in Ruby, Active Record,
                Rails conventions, and the ecosystem. You write clean, efficient,
                and idiomatic Rails code.""",
            goal="Implement Rails features according to architecture",
        )
    
    def rails_tester(self, tools: List) -> Agent:
        return self.create_tester(
            tools=tools,
            backstory="""\
                Rails testing expert specializing in RSpec, MiniTest, Capybara,
                and Factory Bot. You ensure comprehensive test coverage for
                models, controllers, and features.""",
            goal="Write comprehensive tests for Rails implementation",
        )
    
    def rails_reviewer(self, tools: List) -> Agent:
        return self.create_reviewer(
            tools=tools,
            backstory="""\
                Senior Rails engineer focused on code quality, performance,
                security, and conventions. You ensure code follows Rails
                best practices.""",
            goal="Review Rails code for quality and security",
        )
