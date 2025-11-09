"""
Toolkit registration and management for Agent Framework.

This module provides utilities to convert FinRobot's data source and functional
modules into Agent Framework-compatible tool functions.
"""

from typing import List, Callable, Any, get_type_hints
from functools import wraps
from pandas import DataFrame
import inspect


def stringify_output(func: Callable) -> Callable:
    """
    Decorator to convert function outputs to strings for Agent Framework.

    Agent Framework tools should return strings. This decorator automatically
    converts DataFrames and other objects to string representations.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function that returns strings
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, DataFrame):
            # Convert DataFrame to readable string
            if len(result) > 100:
                return f"DataFrame with {len(result)} rows (showing first 100):\n\n{result.head(100).to_string()}"
            return result.to_string()
        elif result is None:
            return "Operation completed successfully."
        else:
            return str(result)

    # Preserve type hints and docstring
    wrapper.__annotations__ = func.__annotations__
    wrapper.__doc__ = func.__doc__

    return wrapper


def create_tool_from_function(
    func: Callable,
    name: str | None = None,
    description: str | None = None,
    auto_stringify: bool = True
) -> Callable:
    """
    Create an Agent Framework compatible tool from a function.

    Args:
        func: Source function
        name: Optional tool name (defaults to function name)
        description: Optional description (defaults to docstring)
        auto_stringify: Automatically apply stringify_output decorator

    Returns:
        Tool function ready for Agent Framework
    """
    tool_func = func

    if auto_stringify:
        tool_func = stringify_output(tool_func)

    # Set metadata
    tool_func.__name__ = name or func.__name__
    tool_func.__doc__ = description or func.__doc__

    return tool_func


def get_tools_from_config(config: List[dict | Callable | type]) -> List[Callable]:
    """
    Convert AutoGen-style tool configuration to Agent Framework tool list.

    Args:
        config: List of tool configurations (functions, classes, or dicts)

    Returns:
        List of tool functions for Agent Framework

    Example:
        >>> tools = get_tools_from_config([
        ...     {"function": get_stock_price, "name": "stock_price"},
        ...     YFinanceUtils,  # class with multiple methods
        ...     get_company_profile,  # direct function
        ... ])
    """
    tools = []

    for item in config:
        if isinstance(item, type):
            # Class - extract all public methods
            tools.extend(get_tools_from_class(item))
        elif callable(item):
            # Direct function
            tools.append(create_tool_from_function(item))
        elif isinstance(item, dict):
            # Dictionary configuration
            func = item.get("function")
            if not func or not callable(func):
                raise ValueError("Dictionary must contain a callable 'function' key")

            tools.append(create_tool_from_function(
                func,
                name=item.get("name"),
                description=item.get("description")
            ))
        else:
            raise ValueError(f"Unsupported tool configuration type: {type(item)}")

    return tools


def get_tools_from_class(
    cls: type,
    include_private: bool = False,
    auto_stringify: bool = True
) -> List[Callable]:
    """
    Extract all methods from a class as Agent Framework tools.

    Args:
        cls: Class to extract methods from
        include_private: Include methods starting with single underscore
        auto_stringify: Apply stringify_output decorator

    Returns:
        List of tool functions

    Example:
        >>> class FinnHubUtils:
        ...     @staticmethod
        ...     def get_company_profile(symbol: str) -> DataFrame:
        ...         ...
        >>> tools = get_tools_from_class(FinnHubUtils)
    """
    tools = []

    for attr_name in dir(cls):
        # Skip magic methods
        if attr_name.startswith("__"):
            continue

        # Skip private methods unless requested
        if not include_private and attr_name.startswith("_"):
            continue

        attr = getattr(cls, attr_name)
        if callable(attr):
            # Handle static methods, class methods, and regular methods
            # For regular (instance) methods, getattr(cls, method_name) returns unbound method
            # which can be called directly as a function
            func = attr

            tools.append(create_tool_from_function(
                func,
                auto_stringify=auto_stringify
            ))

    return tools


def create_toolkit_registry(toolkit_configs: dict[str, List]) -> dict[str, List[Callable]]:
    """
    Create a registry of named toolkits.

    Args:
        toolkit_configs: Dictionary mapping toolkit names to configurations

    Returns:
        Dictionary mapping toolkit names to tool function lists

    Example:
        >>> registry = create_toolkit_registry({
        ...     "market_data": [FinnHubUtils, YFinanceUtils],
        ...     "reporting": [get_sec_report, generate_pdf],
        ... })
        >>> market_tools = registry["market_data"]
    """
    registry = {}

    for toolkit_name, config in toolkit_configs.items():
        registry[toolkit_name] = get_tools_from_config(config)

    return registry


# Common toolkit configurations
def get_coding_tools() -> List[Callable]:
    """Get tools for code generation and file manipulation."""
    from finrobot.functional.coding import CodingUtils

    return get_tools_from_config([
        {"function": CodingUtils.list_dir, "name": "list_files", "description": "List files in a directory."},
        {"function": CodingUtils.see_file, "name": "see_file", "description": "Check the contents of a chosen file."},
        {"function": CodingUtils.modify_code, "name": "modify_code", "description": "Replace old piece of code with new one."},
        {"function": CodingUtils.create_file_with_code, "name": "create_file_with_code", "description": "Create a new file with provided code."},
    ])


def get_market_data_tools() -> List[Callable]:
    """Get tools for market data retrieval."""
    from finrobot.data_source.finnhub_utils import FinnHubUtils
    from finrobot.data_source.yfinance_utils import YFinanceUtils

    return get_tools_from_config([FinnHubUtils, YFinanceUtils])


def get_sec_tools() -> List[Callable]:
    """Get tools for SEC filings analysis."""
    from finrobot.data_source.sec_utils import SECUtils

    return get_tools_from_config([SECUtils])


def get_analysis_tools() -> List[Callable]:
    """Get tools for financial analysis."""
    from finrobot.functional.analyzer import ReportAnalysisUtils

    return get_tools_from_config([ReportAnalysisUtils])


def get_charting_tools() -> List[Callable]:
    """Get tools for financial charting."""
    from finrobot.functional.charting import ReportChartUtils

    return get_tools_from_config([ReportChartUtils])


def get_reporting_tools() -> List[Callable]:
    """Get tools for report generation."""
    from finrobot.functional.reportlab import ReportLabUtils

    return get_tools_from_config([ReportLabUtils])
