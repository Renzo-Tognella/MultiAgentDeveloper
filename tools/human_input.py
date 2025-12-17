"""
Human input tool for agent-user interaction via Slack.
Allows agents to ask clarifying questions during development.
"""
import logging
from typing import Optional

from langchain.tools import tool

logger = logging.getLogger(__name__)

# Global reference to the interaction service (set by orchestrator)
_interaction_service = None


def set_interaction_service(service) -> None:
    """Set the global interaction service instance."""
    global _interaction_service
    _interaction_service = service


def get_interaction_service():
    """Get the global interaction service instance."""
    return _interaction_service


class HumanInputTool:
    """Tool for agents to request human input via Slack."""
    
    @staticmethod
    @tool("Ask User Question")
    def ask_user(question: str, context: str = "") -> str:
        """
        Ask a question to the user and wait for their response.
        Use this when you need clarification or additional information
        to properly implement the solution.
        
        Args:
            question: The question to ask the user
            context: Optional context about why you're asking
        
        Returns:
            The user's response
        """
        service = get_interaction_service()
        
        if service is None:
            logger.warning("No interaction service configured, using console fallback")
            print(f"\n❓ Agent Question: {question}")
            if context:
                print(f"   Context: {context}")
            return input("📝 Your answer: ").strip()
        
        return service.ask_question(question, context)
    
    @staticmethod
    @tool("Send Status Update")
    def send_update(message: str) -> str:
        """
        Send a status update to the user about current progress.
        Use this to keep the user informed about what you're working on.
        
        Args:
            message: The status message to send
        
        Returns:
            Confirmation that the message was sent
        """
        service = get_interaction_service()
        
        if service is None:
            logger.info(f"Status update: {message}")
            print(f"\n📊 Status: {message}")
            return "Update logged to console"
        
        service.send_update(message)
        return "Status update sent to user"


class InteractiveAgentMixin:
    """
    Mixin that provides human interaction capabilities to agents.
    Use this to enable agents to ask questions during their work.
    """
    
    @staticmethod
    def get_human_tools() -> list:
        """Get tools for human interaction."""
        return [
            HumanInputTool.ask_user,
            HumanInputTool.send_update,
        ]
