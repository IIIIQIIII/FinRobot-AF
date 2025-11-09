"""
Response utilities for Agent Framework workflows.

Helper functions to extract meaningful content from various response types.
"""

from typing import Any


def extract_response_text(response: Any) -> str:
    """
    Extract text from various Agent Framework response types.

    Args:
        response: Response from agent.run() or workflow.run()

    Returns:
        String representation of the response
    """
    # If it's a simple object with .text attribute
    if hasattr(response, 'text'):
        return response.text

    # If it's a list of events (from GroupChat workflow)
    if isinstance(response, list):
        text_parts = []
        for event in response:
            # Look for WorkflowOutputEvent
            if hasattr(event, '__class__') and 'WorkflowOutputEvent' in event.__class__.__name__:
                if hasattr(event, 'data'):
                    data = event.data
                    if hasattr(data, 'content'):
                        if isinstance(data.content, str):
                            text_parts.append(data.content)
                        elif isinstance(data.content, list):
                            for item in data.content:
                                if hasattr(item, 'text'):
                                    text_parts.append(item.text)
                                elif isinstance(item, str):
                                    text_parts.append(item)

        if text_parts:
            return "\n\n".join(text_parts)

        # Fallback: just describe the events
        event_types = [type(e).__name__ for e in response]
        return f"Workflow completed with events: {', '.join(event_types)}"

    # If it's a dict
    if isinstance(response, dict):
        if 'text' in response:
            return response['text']
        if 'content' in response:
            return str(response['content'])
        return str(response)

    # Fallback: convert to string
    return str(response)


def format_multi_agent_response(response: Any) -> str:
    """
    Format multi-agent response for display.

    Args:
        response: Response from multi-agent workflow

    Returns:
        Formatted string
    """
    text = extract_response_text(response)

    # Add header if it looks like multiple agents contributed
    if '\n\n' in text or len(text) > 200:
        return f"Multi-Agent Response:\n{'=' * 60}\n{text}\n{'=' * 60}"
    else:
        return text
