"""React framework tasks."""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class ReactTasks(BaseTasks):
    """Factory for React-specific tasks."""
    
    @property
    def framework_name(self) -> str:
        return "React"
    
    def react_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design React component architecture for:
                
                REQUIREMENTS: {requirements}
                FILES TO MODIFY: {files_to_modify}
                FILES TO CREATE: {files_to_create}
                
                Include:
                1. Component hierarchy and structure
                2. State management approach
                3. Props flow and data handling
                4. Hooks to use
                5. Integration points
                
                {incentive}""",
            expected_output="Detailed React architecture document with component structure",
        )
    
    def react_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement React components per architecture:
                
                1. Create React components (.jsx/.js)
                2. Implement hooks and state management
                3. Add PropTypes or TypeScript interfaces
                4. Include error handling and loading states
                5. Follow React best practices""",
            expected_output="Complete React component files",
        )
    
    def react_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Write tests for React components:
                
                1. Use Jest and React Testing Library
                2. Test rendering, props, interactions
                3. Test hooks and state management
                4. Include edge cases
                5. Mock external dependencies""",
            expected_output="Test files with comprehensive coverage",
        )
    
    def react_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review React implementation:
                
                1. Code follows React conventions
                2. Components properly structured
                3. Performance considerations
                4. Accessibility compliance
                5. Error boundaries
                6. Documentation""",
            expected_output="Review report with feedback and run instructions",
        )
