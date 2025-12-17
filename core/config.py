"""
Centralized configuration management.
Following Clean Architecture principles - configuration is an infrastructure concern.
"""
import os
import logging
from dataclasses import dataclass
from typing import Optional
from decouple import config


@dataclass(frozen=True)
class Settings:
    """Application settings - immutable configuration object."""
    
    # OpenAI settings
    openai_api_key: str
    openai_model: str = "gpt-4o"
    openai_temperature: float = 0.3
    serper_api_key: Optional[str] = None
    
    # Slack settings
    slack_token: Optional[str] = None
    slack_channel: str = ""
    slack_enabled: bool = False
    slack_poll_interval: int = 5
    slack_timeout: int = 300
    
    # General settings
    log_level: str = "INFO"
    verbose_agents: bool = False
    
    def __post_init__(self):
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key
    
    @property
    def is_slack_configured(self) -> bool:
        """Check if Slack is properly configured."""
        return bool(self.slack_enabled and self.slack_token and self.slack_channel)


def load_settings() -> Settings:
    """Load settings from environment variables."""
    return Settings(
        openai_api_key=config("OPENAI_API_KEY", default=""),
        openai_model=config("OPENAI_MODEL", default="gpt-4o"),
        openai_temperature=config("OPENAI_TEMPERATURE", default=0.3, cast=float),
        serper_api_key=config("SERPER_API_KEY", default=None),
        slack_token=config("SLACK_BOT_TOKEN", default=None),
        slack_channel=config("SLACK_CHANNEL", default=""),
        slack_enabled=config("SLACK_ENABLED", default=False, cast=bool),
        slack_poll_interval=config("SLACK_POLL_INTERVAL", default=5, cast=int),
        slack_timeout=config("SLACK_TIMEOUT", default=300, cast=int),
        log_level=config("LOG_LEVEL", default="INFO"),
        verbose_agents=config("VERBOSE_AGENTS", default=False, cast=bool),
    )


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("langchain").setLevel(logging.WARNING)
    
    return logging.getLogger("multiagent")
