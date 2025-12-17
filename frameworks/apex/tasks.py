"""Apex/Salesforce framework tasks."""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class ApexTasks(BaseTasks):
    """Factory for Apex-specific tasks."""
    
    @property
    def framework_name(self) -> str:
        return "Salesforce Apex"
    
    def apex_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design Salesforce architecture for:
                
                REQUIREMENTS: {requirements}
                FILES TO MODIFY: {files_to_modify}
                FILES TO CREATE: {files_to_create}
                
                Include:
                1. Apex classes and patterns
                2. Trigger framework
                3. LWC structure
                4. SOQL patterns
                5. Governor Limits planning
                
                {incentive}""",
            expected_output="Detailed Salesforce architecture document",
        )
    
    def apex_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement Salesforce solution per architecture:
                
                1. Create Apex classes
                2. Implement bulkified triggers
                3. Build LWC components
                4. Write efficient SOQL
                5. Include metadata XML""",
            expected_output="Complete Salesforce implementation",
        )
    
    def apex_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Write tests for Salesforce implementation:
                
                1. Test classes for Apex
                2. Bulk trigger tests
                3. Use Test.startTest/stopTest
                4. Test data factories
                5. 75%+ coverage""",
            expected_output="Apex test classes with coverage",
        )
    
    def apex_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review Salesforce implementation:
                
                1. Governor Limits compliance
                2. Bulkification
                3. CRUD/FLS security
                4. SOQL optimization
                5. Exception handling""",
            expected_output="Review report with deployment docs",
        )
