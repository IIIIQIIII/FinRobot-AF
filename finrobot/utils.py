"""
FinRobot utility functions for Agent Framework.

This module provides common utilities for date handling, file operations,
API key management, and type definitions.
"""

import os
import json
import pandas as pd
from datetime import date, timedelta, datetime
from typing import Annotated, Optional
from pydantic import Field


# Define custom annotated types for Agent Framework tool parameters
SavePathType = Annotated[str, Field(description="File path to save data. If None, data is not saved.")]


def save_output(data: pd.DataFrame, tag: str, save_path: Optional[str] = None) -> None:
    """
    Save DataFrame to CSV file.

    Args:
        data: DataFrame to save
        tag: Description tag for the data
        save_path: File path to save data. If None, data is not saved.
    """
    if save_path:
        data.to_csv(save_path)
        print(f"{tag} saved to {save_path}")


def get_current_date() -> str:
    """
    Get current date in YYYY-MM-DD format.

    Returns:
        Current date as string
    """
    return date.today().strftime("%Y-%m-%d")


def register_keys_from_json(file_path: str) -> None:
    """
    Load API keys from JSON file and register them as environment variables.

    Args:
        file_path: Path to JSON file containing API keys

    Expected JSON format:
    {
        "OPENAI_API_KEY": "sk-...",
        "FINNHUB_API_KEY": "...",
        "FMP_API_KEY": "...",
        "SEC_API_KEY": "..."
    }
    """
    with open(file_path, "r") as f:
        keys = json.load(f)
    for key, value in keys.items():
        os.environ[key] = value


def decorate_all_methods(decorator):
    """
    Class decorator to apply a decorator to all methods of a class.

    Args:
        decorator: Decorator function to apply

    Returns:
        Class decorator function
    """
    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("_"):
                setattr(cls, attr_name, decorator(attr_value))
        return cls
    return class_decorator


def get_next_weekday(input_date) -> datetime:
    """
    Get next weekday if the given date falls on weekend.

    Args:
        input_date: Date as string (YYYY-MM-DD) or datetime object

    Returns:
        Next weekday as datetime object
    """
    if not isinstance(input_date, datetime):
        input_date = datetime.strptime(input_date, "%Y-%m-%d")

    if input_date.weekday() >= 5:  # Saturday or Sunday
        days_to_add = 7 - input_date.weekday()
        next_weekday = input_date + timedelta(days=days_to_add)
        return next_weekday
    else:
        return input_date


def dataframe_to_string(df: pd.DataFrame, max_rows: int = 100) -> str:
    """
    Convert DataFrame to string representation for Agent Framework tools.

    Agent Framework tools should return strings, not DataFrames.
    This utility function converts DataFrames to formatted strings.

    Args:
        df: DataFrame to convert
        max_rows: Maximum number of rows to include

    Returns:
        String representation of DataFrame
    """
    if len(df) > max_rows:
        return f"DataFrame with {len(df)} rows (showing first {max_rows}):\n\n{df.head(max_rows).to_string()}"
    return df.to_string()


def load_llm_config(config_path: str = "OAI_CONFIG_LIST") -> dict:
    """
    Load LLM configuration from JSON file.

    Args:
        config_path: Path to config file

    Returns:
        Dictionary with model configuration

    Expected format:
    [
        {
            "model": "gpt-4",
            "api_key": "sk-...",
            "base_url": "https://api.openai.com/v1"  # optional
        }
    ]
    """
    with open(config_path, "r") as f:
        config_list = json.load(f)

    if isinstance(config_list, list):
        return config_list[0]
    return config_list


def create_chat_client(config: Optional[dict] = None, config_path: str = "OAI_CONFIG_LIST"):
    """
    Create OpenAI chat client for Agent Framework.

    Args:
        config: Optional config dict. If None, loads from config_path
        config_path: Path to config file if config is None

    Returns:
        OpenAIChatClient instance
    """
    from agent_framework.openai import OpenAIChatClient

    if config is None:
        config = load_llm_config(config_path)

    return OpenAIChatClient(
        model_id=config.get("model", "gpt-4"),
        api_key=config.get("api_key"),
        base_url=config.get("base_url")
    )
