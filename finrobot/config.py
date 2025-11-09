"""
Configuration management for FinRobot Agent Framework.

Handles API keys, LLM configurations, and environment setup.
"""

import os
import json
from typing import Optional, Dict, Any
from pathlib import Path


class FinRobotConfig:
    """
    Central configuration manager for FinRobot.

    Manages API keys, LLM client configuration, and environment variables.
    """

    def __init__(
        self,
        api_keys_path: Optional[str] = None,
        llm_config_path: Optional[str] = None
    ):
        """
        Initialize configuration.

        Args:
            api_keys_path: Path to JSON file with API keys (e.g., config_api_keys)
            llm_config_path: Path to LLM config file (e.g., OAI_CONFIG_LIST)
        """
        self.api_keys_path = api_keys_path or "config_api_keys"
        self.llm_config_path = llm_config_path or "OAI_CONFIG_LIST"

        self._api_keys: Dict[str, str] = {}
        self._llm_config: Dict[str, Any] = {}
        self._chat_client = None

    def load_api_keys(self, path: Optional[str] = None) -> None:
        """
        Load API keys from JSON file and set as environment variables.

        Args:
            path: Optional override path to API keys file
        """
        file_path = path or self.api_keys_path

        if not os.path.exists(file_path):
            print(f"Warning: API keys file not found at {file_path}")
            return

        with open(file_path, "r") as f:
            self._api_keys = json.load(f)

        # Set environment variables
        for key, value in self._api_keys.items():
            os.environ[key] = value

        print(f"Loaded {len(self._api_keys)} API keys from {file_path}")

    def load_llm_config(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load LLM configuration from JSON file.

        Args:
            path: Optional override path to LLM config file

        Returns:
            Dictionary with model configuration
        """
        file_path = path or self.llm_config_path

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"LLM config file not found at {file_path}")

        with open(file_path, "r") as f:
            config = json.load(f)

        # Handle both list and dict formats
        if isinstance(config, list):
            self._llm_config = config[0] if config else {}
        else:
            self._llm_config = config

        return self._llm_config

    def get_chat_client(self, model_id: Optional[str] = None):
        """
        Get or create OpenAI chat client.

        Args:
            model_id: Optional model ID override

        Returns:
            OpenAIChatClient instance
        """
        from agent_framework.openai import OpenAIChatClient

        if self._chat_client is not None and model_id is None:
            return self._chat_client

        if not self._llm_config:
            self.load_llm_config()

        client = OpenAIChatClient(
            model_id=model_id or self._llm_config.get("model", "gpt-4"),
            api_key=self._llm_config.get("api_key") or os.getenv("OPENAI_API_KEY"),
            base_url=self._llm_config.get("base_url")
        )

        if model_id is None:
            self._chat_client = client

        return client

    def get_api_key(self, key_name: str) -> Optional[str]:
        """
        Get API key by name.

        Args:
            key_name: Name of the API key

        Returns:
            API key value or None if not found
        """
        # First check environment
        if key_name in os.environ:
            return os.environ[key_name]

        # Then check loaded keys
        if key_name in self._api_keys:
            return self._api_keys[key_name]

        return None

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


def initialize_config(
    api_keys_path: Optional[str] = None,
    llm_config_path: Optional[str] = None,
    auto_load: bool = True
) -> FinRobotConfig:
    """
    Initialize global configuration.

    Args:
        api_keys_path: Path to API keys JSON file
        llm_config_path: Path to LLM config JSON file
        auto_load: Automatically load API keys and LLM config

    Returns:
        Initialized FinRobotConfig instance

    Example:
        >>> config = initialize_config(
        ...     api_keys_path="config_api_keys",
        ...     llm_config_path="OAI_CONFIG_LIST"
        ... )
        >>> client = config.get_chat_client()
    """
    global _global_config
    _global_config = FinRobotConfig(
        api_keys_path=api_keys_path,
        llm_config_path=llm_config_path
    )

    if auto_load:
        _global_config.load_api_keys()
        _global_config.load_llm_config()

    return _global_config
