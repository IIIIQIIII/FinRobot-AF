"""
Workflow Configuration Manager
===============================

Load and manage configurable workflows with different LLM providers
per step.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class WorkflowConfig:
    """Manages workflow configurations."""

    def __init__(self, workflow_name: str, config_path: Optional[str] = None):
        """
        Initialize workflow configuration.

        Args:
            workflow_name: Name of the workflow (e.g., "sentiment_analysis")
            config_path: Optional path to config file
        """
        self.workflow_name = workflow_name

        if config_path is None:
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "config" / "workflows" / f"{workflow_name}.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load workflow configuration from JSON."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Workflow config not found: {self.config_path}\n"
                f"Create config/workflows/{self.workflow_name}.json"
            )

        with open(self.config_path) as f:
            return json.load(f)

    def get_step_config(self, step_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific step.

        Args:
            step_name: Name of the step (e.g., "extraction", "sentiment")

        Returns:
            Step configuration dict
        """
        if step_name not in self.config.get("steps", {}):
            raise KeyError(f"Step '{step_name}' not found in workflow config")

        return self.config["steps"][step_name]

    def get_llm_config(self, step_name: str) -> Dict[str, Any]:
        """
        Get LLM configuration for a step.

        Args:
            step_name: Name of the step

        Returns:
            LLM config with provider, model, temperature, etc.
        """
        step = self.get_step_config(step_name)

        return {
            "provider": step.get("llm_provider", "openrouter"),
            "model": step.get("llm_model", "gpt-4"),
            "temperature": step.get("temperature", 0.7),
            "max_tokens": step.get("max_tokens", 2000),
            "agent_name": step.get("agent_name", "Assistant")
        }

    def get_paths(self) -> Dict[str, Any]:
        """Get input/output paths configuration."""
        paths = self.config.get("paths", {})

        # Make paths absolute
        base_dir = Path(__file__).parent.parent

        return {
            "input_folder": base_dir / paths.get("input_folder", "data/10k_filings"),
            "output_folder": base_dir / paths.get("output_folder", "results"),
            "save_intermediate": paths.get("save_intermediate", True)
        }

    def get_options(self) -> Dict[str, Any]:
        """Get workflow options."""
        return self.config.get("options", {})

    def get_all_steps(self) -> list:
        """Get list of all step names."""
        return list(self.config.get("steps", {}).keys())

    def __repr__(self):
        return f"WorkflowConfig('{self.workflow_name}')"


def load_workflow(workflow_name: str) -> WorkflowConfig:
    """
    Quick helper to load a workflow config.

    Args:
        workflow_name: Name of the workflow

    Returns:
        WorkflowConfig instance

    Example:
        >>> config = load_workflow("sentiment_analysis")
        >>> extraction_config = config.get_llm_config("extraction")
    """
    return WorkflowConfig(workflow_name)
