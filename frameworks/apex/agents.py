"""Apex/Salesforce framework agents."""
from typing import List
from crewai import Agent
from frameworks.base import BaseAgents


class ApexAgents(BaseAgents):
    """Factory for Apex-specific agents."""
    
    @property
    def framework_name(self) -> str:
        return "Salesforce Apex"
    
    def apex_architect(self, tools: List) -> Agent:
        return self.create_architect(
            tools=tools,
            backstory="""\
                Senior Salesforce architect with expertise in Apex, Visualforce,
                LWC, and Governor Limits. You design scalable solutions within
                platform constraints.""",
            goal="Design Salesforce architecture including Apex classes and triggers",
        )
    
    def apex_programmer(self, tools: List) -> Agent:
        return self.create_programmer(
            tools=tools,
            backstory="""\
                Expert Salesforce developer with experience in Apex, SOQL, SOSL,
                LWC, and APIs. You write efficient code respecting Governor Limits.""",
            goal="Implement Apex classes, triggers, and LWC components",
        )
    
    def apex_tester(self, tools: List) -> Agent:
        return self.create_tester(
            tools=tools,
            backstory="""\
                Salesforce testing expert specializing in Apex test classes,
                test data factories, and code coverage. You ensure comprehensive
                testing within Governor Limits.""",
            goal="Write comprehensive Apex test classes",
        )
    
    def apex_reviewer(self, tools: List) -> Agent:
        return self.create_reviewer(
            tools=tools,
            backstory="""\
                Senior Salesforce architect focused on security, Governor Limits,
                performance, and best practices. You ensure code meets platform
                standards.""",
            goal="Review Salesforce code for limits and security",
        )
