"""Frontend (HTML/CSS/JS) framework agents."""
from typing import List
from crewai import Agent
from frameworks.base import BaseAgents


class FrontendAgents(BaseAgents):
    """Factory for Frontend-specific agents."""
    
    @property
    def framework_name(self) -> str:
        return "Frontend"
    
    def frontend_architect(self, tools: List) -> Agent:
        return self.create_architect(
            tools=tools,
            backstory="""\
                Senior frontend architect with expertise in HTML5, CSS3, ES6+,
                responsive design, and modern patterns. You create accessible
                and performant interfaces.""",
            goal="Design frontend structure and technical approach",
        )
    
    def frontend_programmer(self, tools: List) -> Agent:
        return self.create_programmer(
            tools=tools,
            backstory="""\
                Expert frontend developer with experience in HTML, CSS, JavaScript,
                DOM manipulation, and cross-browser compatibility. You write clean,
                semantic code.""",
            goal="Implement HTML, CSS, and JavaScript per architecture",
        )
    
    def frontend_tester(self, tools: List) -> Agent:
        return self.create_tester(
            tools=tools,
            backstory="""\
                Frontend testing expert specializing in Jest, Mocha, Cypress,
                and browser testing. You ensure UI coverage and cross-browser
                compatibility.""",
            goal="Write comprehensive frontend tests",
        )
    
    def frontend_reviewer(self, tools: List) -> Agent:
        return self.create_reviewer(
            tools=tools,
            backstory="""\
                Senior frontend engineer focused on performance, accessibility,
                SEO, and web standards. You ensure excellent user experience.""",
            goal="Review frontend code for quality and accessibility",
        )
