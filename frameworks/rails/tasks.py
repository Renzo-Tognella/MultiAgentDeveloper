"""Ruby on Rails framework tasks."""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class RailsTasks(BaseTasks):
    """Factory for Rails-specific tasks."""
    
    @property
    def framework_name(self) -> str:
        return "Ruby on Rails"
    
    def rails_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design Rails architecture for:
                
                REQUIREMENTS: {requirements}
                FILES TO MODIFY: {files_to_modify}
                FILES TO CREATE: {files_to_create}
                
                Include:
                1. Models and associations
                2. Controllers and actions
                3. Routes configuration
                4. Database migrations
                5. Business logic placement
                
                {incentive}""",
            expected_output="Detailed Rails architecture document",
        )
    
    def rails_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement Rails features per architecture:
                
                1. Create models with validations
                2. Implement RESTful controllers
                3. Configure routes
                4. Create migrations
                5. Build views with ERB""",
            expected_output="Complete Rails implementation",
        )
    
    def rails_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Write tests for Rails implementation:
                
                1. Model specs with validations
                2. Controller tests
                3. Request/integration tests
                4. Factory definitions
                5. Edge cases""",
            expected_output="RSpec test files with coverage",
        )
    
    def rails_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review Rails implementation:
                
                1. Follows Rails conventions
                2. Proper Active Record usage
                3. Security considerations
                4. N+1 query prevention
                5. Error handling""",
            expected_output="Review report with feedback",
        )
