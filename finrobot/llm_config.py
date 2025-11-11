"""
LLM Provider Configuration Manager
===================================

Support multiple LLM providers:
- OpenRouter (GPT-4, GPT-5, Claude, etc.)
- Aliyun Bailian (阿里云百炼 - Qwen models)
- OpenAI Direct

Usage:
    from finrobot.llm_config import LLMConfigManager

    # Load config
    config_mgr = LLMConfigManager()

    # Get active provider config
    llm_config = config_mgr.get_active_config()

    # Switch provider
    config_mgr.set_active_provider("aliyun", "qwen-max")

    # Create chat client
    client = config_mgr.get_chat_client()
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def load_dotenv(dotenv_path: Optional[Path] = None):
    """Load environment variables from .env file."""
    if dotenv_path is None:
        # Try to find .env in project root
        current = Path(__file__).parent.parent
        dotenv_path = current / ".env"

    if not dotenv_path.exists():
        return

    with open(dotenv_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Only set if not already in environment
                if key not in os.environ:
                    os.environ[key] = value


class LLMConfigManager:
    """Manage multiple LLM provider configurations."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config manager.

        Args:
            config_path: Path to llm_providers.json (default: config/llm_providers.json)
        """
        # Load .env file first
        load_dotenv()

        if config_path is None:
            # Try to find config relative to this file
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "config" / "llm_providers.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"LLM provider config not found at {self.config_path}\n"
                f"Please create config/llm_providers.json"
            )

        with open(self.config_path) as f:
            return json.load(f)

    def _save_config(self) -> None:
        """Save configuration to JSON file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific provider.

        Args:
            provider_name: Provider name (e.g., "openrouter", "aliyun", "openai")

        Returns:
            Provider configuration dictionary

        Raises:
            KeyError: If provider not found
        """
        if provider_name not in self.config["providers"]:
            available = ", ".join(self.config["providers"].keys())
            raise KeyError(
                f"Provider '{provider_name}' not found. "
                f"Available: {available}"
            )

        return self.config["providers"][provider_name]

    def get_active_config(self) -> Dict[str, Any]:
        """
        Get configuration for active provider and model.

        Returns:
            Dictionary with model, api_key, base_url for OpenAI-compatible client
        """
        provider_name = self.config["active_provider"]
        model_name = self.config["active_model"]

        provider = self.get_provider_config(provider_name)

        # Get model ID (use mapping or direct name)
        if model_name in provider["models"]:
            model_id = provider["models"][model_name]
        else:
            # Fallback to default
            model_id = provider["models"]["default"]

        # Handle environment variable substitution
        api_key = provider["api_key"]
        if api_key.startswith("${") and api_key.endswith("}"):
            env_var = api_key[2:-1]
            api_key = os.getenv(env_var)
            if not api_key:
                raise ValueError(
                    f"Environment variable {env_var} not set for provider {provider_name}"
                )

        return {
            "model": model_id,
            "api_key": api_key,
            "base_url": provider["base_url"],
            "provider_name": provider["name"]
        }

    def set_active_provider(
        self,
        provider_name: str,
        model_name: Optional[str] = None
    ) -> None:
        """
        Set active provider and model.

        Args:
            provider_name: Provider name (e.g., "aliyun", "openrouter")
            model_name: Model name (e.g., "qwen-max", "gpt-5"). If None, uses provider's default.
        """
        # Validate provider exists
        provider = self.get_provider_config(provider_name)

        # If no model specified, use default
        if model_name is None:
            model_name = list(provider["models"].keys())[0]
            # Prefer "default" if available
            if "default" in provider["models"]:
                for key in provider["models"]:
                    if key != "default":
                        model_name = key
                        break

        # Validate model exists for provider
        if model_name not in provider["models"]:
            available = ", ".join(
                k for k in provider["models"].keys() if k != "default"
            )
            raise KeyError(
                f"Model '{model_name}' not available for {provider_name}. "
                f"Available: {available}"
            )

        # Update config
        self.config["active_provider"] = provider_name
        self.config["active_model"] = model_name
        self._save_config()

        print(f"✓ Switched to {provider['name']}: {model_name}")

    def get_chat_client(self, model_override: Optional[str] = None):
        """
        Get OpenAI-compatible chat client for active provider.

        Args:
            model_override: Optional model override

        Returns:
            OpenAIChatClient instance
        """
        from agent_framework.openai import OpenAIChatClient

        config = self.get_active_config()

        return OpenAIChatClient(
            model_id=model_override or config["model"],
            api_key=config["api_key"],
            base_url=config["base_url"]
        )

    def list_providers(self) -> None:
        """Print available providers and models."""
        print("\n" + "="*60)
        print("Available LLM Providers")
        print("="*60)

        active_provider = self.config["active_provider"]
        active_model = self.config["active_model"]

        for name, provider in self.config["providers"].items():
            marker = "✓" if name == active_provider else " "
            print(f"\n{marker} {provider['name']} ({name})")
            print(f"  Base URL: {provider['base_url']}")
            print(f"  Models:")

            for model_key, model_id in provider["models"].items():
                if model_key == "default":
                    continue
                model_marker = "→" if (name == active_provider and model_key == active_model) else " "
                print(f"    {model_marker} {model_key}: {model_id}")

        print("\n" + "="*60)
        print(f"Active: {active_provider} / {active_model}")
        print("="*60 + "\n")


def get_llm_config() -> Dict[str, Any]:
    """
    Quick helper to get active LLM configuration.

    Returns:
        Configuration dict for OpenAI-compatible client

    Example:
        >>> config = get_llm_config()
        >>> client = OpenAIChatClient(**config)
    """
    mgr = LLMConfigManager()
    return mgr.get_active_config()


def switch_provider(provider: str, model: Optional[str] = None) -> None:
    """
    Quick helper to switch active provider.

    Args:
        provider: Provider name (aliyun, openrouter, openai)
        model: Model name (optional)

    Example:
        >>> switch_provider("aliyun", "qwen-max")
        >>> switch_provider("openrouter", "gpt-5")
    """
    mgr = LLMConfigManager()
    mgr.set_active_provider(provider, model)


if __name__ == "__main__":
    # Demo
    mgr = LLMConfigManager()
    mgr.list_providers()
