"""
Configuration management for FinRobot Agent Framework.

Handles API keys, LLM configurations, and environment setup.
Uses .env file for configuration management.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv


class FinRobotConfig:
    """
    Central configuration manager for FinRobot.

    Manages API keys, LLM client configuration, and environment variables.
    """

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            env_file: Path to .env file (default: .env in project root)
        """
        self.env_file = env_file or ".env"
        self._chat_client = None

        # Load environment variables from .env file
        self._load_env()

    def _load_env(self) -> None:
        """
        Load environment variables from .env file.
        """
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            print(f"✓ Loaded environment from {self.env_file}")
        else:
            # Try to load from default locations
            if os.path.exists(".env"):
                load_dotenv(".env")
                print("✓ Loaded environment from .env")
            else:
                print("⚠️  No .env file found, using system environment variables")

    def get_chat_client(self, model_id: Optional[str] = None, use_provider_config: bool = True):
        """
        Get or create OpenAI chat client.

        Args:
            model_id: Optional model ID override
            use_provider_config: If True, use config/llm_providers.json (new system)

        Returns:
            OpenAIChatClient instance
        """
        from agent_framework.openai import OpenAIChatClient

        # Try new provider config system first
        if use_provider_config:
            try:
                from finrobot.llm_config import LLMConfigManager
                mgr = LLMConfigManager()
                config = mgr.get_active_config()

                client = OpenAIChatClient(
                    model_id=model_id or config["model"],
                    api_key=config["api_key"],
                    base_url=config["base_url"]
                )

                if model_id is None:
                    self._chat_client = client

                return client
            except (FileNotFoundError, ImportError):
                # Fall back to environment variables
                print("⚠️  Provider config not found, using environment variables")

        # Use environment variables from .env
        if self._chat_client is not None and model_id is None:
            return self._chat_client

        # Default to OpenAI from environment
        client = OpenAIChatClient(
            model_id=model_id or os.getenv("OPENAI_MODEL", "gpt-4"),
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

        if model_id is None:
            self._chat_client = client

        return client

    def get_api_key(self, key_name: str) -> Optional[str]:
        """
        Get API key by name from environment variables.

        Args:
            key_name: Name of the API key

        Returns:
            API key value or None if not found
        """
        return os.getenv(key_name)

    @property
    def finnhub_api_key(self) -> Optional[str]:
        """Get FinnHub API key."""
        return self.get_api_key("FINNHUB_API_KEY")

    @property
    def fmp_api_key(self) -> Optional[str]:
        """Get Financial Modeling Prep API key."""
        return self.get_api_key("FMP_API_KEY")

    @property
    def sec_api_key(self) -> Optional[str]:
        """Get SEC API key."""
        return self.get_api_key("SEC_API_KEY")

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key."""
        return self.get_api_key("OPENAI_API_KEY")


# Global config instance
_global_config: Optional[FinRobotConfig] = None


def get_config() -> FinRobotConfig:
    """
    Get global FinRobot configuration instance.

    Returns:
        Global FinRobotConfig instance
    """
    global _global_config
    if _global_config is None:
        _global_config = FinRobotConfig()
    return _global_config


def initialize_config(env_file: Optional[str] = None) -> FinRobotConfig:
    """
    Initialize global configuration from .env file.

    Args:
        env_file: Path to .env file (default: .env in project root)

    Returns:
        Initialized FinRobotConfig instance

    Example:
        >>> config = initialize_config()  # Loads from .env
        >>> client = config.get_chat_client()
    """
    global _global_config
    _global_config = FinRobotConfig(env_file=env_file)
    return _global_config
