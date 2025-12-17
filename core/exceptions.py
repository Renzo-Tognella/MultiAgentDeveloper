"""
Custom exceptions for the MultiAgent Developer application.
Following Clean Architecture - domain exceptions are separate from infrastructure.
"""


class MultiAgentError(Exception):
    """Base exception for MultiAgent Developer."""
    pass


class ConfigurationError(MultiAgentError):
    """Raised when configuration is invalid or missing."""
    pass


class ParsingError(MultiAgentError):
    """Raised when parsing a backlog card fails."""
    pass


class OrchestrationError(MultiAgentError):
    """Raised when orchestration fails."""
    pass


class FrameworkNotSupportedError(MultiAgentError):
    """Raised when the detected framework is not supported."""
    pass
