"""Frontend (HTML/CSS/JS) framework tasks."""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class FrontendTasks(BaseTasks):
    """Factory for Frontend-specific tasks."""
    
    @property
    def framework_name(self) -> str:
        return "Frontend"
    
    def frontend_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design frontend architecture for:
                
                REQUIREMENTS: {requirements}
                FILES TO MODIFY: {files_to_modify}
                FILES TO CREATE: {files_to_create}
                
                Include:
                1. HTML structure
                2. CSS architecture
                3. JavaScript modules
                4. Responsive approach
                5. Accessibility plan
                
                {incentive}""",
            expected_output="Detailed frontend architecture document",
        )
    
    def frontend_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement frontend per architecture:
                
                1. Semantic HTML5
                2. Responsive CSS
                3. Modern JavaScript (ES6+)
                4. Cross-browser support
                5. ARIA accessibility""",
            expected_output="Complete frontend implementation",
        )
    
    def frontend_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Write tests for frontend implementation:
                
                1. JavaScript unit tests
                2. Accessibility tests
                3. Responsive verification
                4. Cross-browser setup
                5. User interactions""",
            expected_output="Test files with coverage",
        )
    
    def frontend_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review frontend implementation:
                
                1. Web standards
                2. Semantic HTML
                3. CSS organization
                4. JS performance
                5. SEO optimization""",
            expected_output="Review report with feedback",
        )
