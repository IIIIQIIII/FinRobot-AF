"""
Workflow patterns for FinRobot Agent Framework.

This module provides workflow orchestration patterns migrated from AutoGen:
- SingleAssistant: Basic agent-user interaction
- SingleAssistantRAG: Agent with retrieval-augmented generation
- SingleAssistantShadow: Dual-agent planning pattern
- MultiAssistant: Group chat with multiple agents
- MultiAssistantWithLeader: Hierarchical multi-agent coordination
"""

from typing import Optional, Dict, Any, List, Callable
from abc import ABC, abstractmethod
from agent_framework import ChatAgent, AgentThread
from finrobot.agents.agent_library import create_agent, create_default_toolkit_registry
from finrobot.config import get_config


class WorkflowBase(ABC):
    """Base class for FinRobot workflows."""

    def __init__(
        self,
        agent_config: str | Dict[str, Any],
        chat_client=None,
        toolkit_registry: Optional[Dict] = None,
    ):
        """
        Initialize workflow with agent configuration.

        Args:
            agent_config: Agent name (string) or configuration dict
            chat_client: Agent Framework chat client
            toolkit_registry: Optional custom toolkit registry
        """
        if chat_client is None:
            config = get_config()
            chat_client = config.get_chat_client()

        self.chat_client = chat_client

        # Use default registry if not provided
        if toolkit_registry is None:
            toolkit_registry = create_default_toolkit_registry()

        self.toolkit_registry = toolkit_registry

        # Create main agent
        if isinstance(agent_config, str):
            self.agent = create_agent(agent_config, chat_client, toolkit_registry)
        else:
            # Custom config - extract name and create
            self.agent = create_agent(
                agent_config.get("name", "CustomAgent"),
                chat_client,
                toolkit_registry
            )

        # Create thread for conversation state
        self.thread = self.agent.get_new_thread()

    @abstractmethod
    async def chat(self, message: str, **kwargs):
        """Execute workflow with given message."""
        pass

    def reset(self):
        """Reset workflow state by creating new thread."""
        self.thread = self.agent.get_new_thread()


class SingleAssistant(WorkflowBase):
    """
    Single agent workflow pattern.

    Equivalent to AutoGen's SingleAssistant with UserProxyAgent.
    Agent executes tools directly (multi-turn tool execution).
    """

    def __init__(
        self,
        agent_config: str | Dict[str, Any],
        chat_client=None,
        toolkit_registry: Optional[Dict] = None,
        max_turns: int = 10,
        **kwargs
    ):
        """
        Initialize single assistant workflow.

        Args:
            agent_config: Agent name or configuration
            chat_client: Chat client instance
            toolkit_registry: Custom toolkit registry
            max_turns: Maximum conversation turns
            **kwargs: Additional arguments
        """
        super().__init__(agent_config, chat_client, toolkit_registry)
        self.max_turns = max_turns

    async def chat(self, message: str, stream: bool = False, **kwargs):
        """
        Run agent chat.

        Args:
            message: User message
            stream: Whether to stream response
            **kwargs: Additional arguments

        Returns:
            AgentRunResponse with agent's reply (or async generator if stream=True)
        """
        if stream:
            # Streaming response - return async generator
            return self.agent.run_stream(message, thread=self.thread)
        else:
            # Non-streaming response
            response = await self.agent.run(message, thread=self.thread)
            return response


class SingleAssistantRAG(WorkflowBase):
    """
    Single agent workflow with RAG (Retrieval-Augmented Generation).

    Equivalent to AutoGen's SingleAssistantRAG with RetrieveUserProxyAgent.
    Retrieves relevant documents before sending query to agent.
    """

    def __init__(
        self,
        agent_config: str | Dict[str, Any],
        chat_client=None,
        toolkit_registry: Optional[Dict] = None,
        docs_path: Optional[str] = None,
        collection_name: str = "finrobot_docs",
        chunk_size: int = 2000,
        top_k: int = 5,
        **kwargs
    ):
        """
        Initialize RAG workflow.

        Args:
            agent_config: Agent name or configuration
            chat_client: Chat client instance
            toolkit_registry: Custom toolkit registry
            docs_path: Path to documents for RAG
            collection_name: Vector store collection name
            chunk_size: Document chunk size
            top_k: Number of documents to retrieve
            **kwargs: Additional arguments
        """
        super().__init__(agent_config, chat_client, toolkit_registry)

        # Initialize RAG components
        self.docs_path = docs_path
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.top_k = top_k
        self.vector_store = None

        if docs_path:
            self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize vector store for RAG."""
        try:
            from finrobot.functional.rag import get_rag_function
            self.rag_retriever = get_rag_function(
                docs_path=self.docs_path,
                collection_name=self.collection_name,
                chunk_token_size=self.chunk_size
            )
        except Exception as e:
            print(f"Warning: Could not initialize RAG vector store: {e}")
            self.rag_retriever = None

    async def chat(self, message: str, stream: bool = False, **kwargs):
        """
        Run agent chat with RAG.

        Args:
            message: User query
            stream: Whether to stream response
            **kwargs: Additional arguments

        Returns:
            AgentRunResponse with agent's reply
        """
        # Retrieve relevant documents
        if self.rag_retriever:
            context_docs = self.rag_retriever(message, n_results=self.top_k)
            context = "\n\n".join(context_docs) if context_docs else ""

            # Enhance message with context
            enhanced_message = f"""Context from documents:
{context}

User query: {message}
"""
        else:
            enhanced_message = message

        # Run agent with enhanced message
        if stream:
            return self.agent.run_stream(enhanced_message, thread=self.thread)
        else:
            response = await self.agent.run(enhanced_message, thread=self.thread)
            return response


class SingleAssistantShadow(WorkflowBase):
    """
    Dual-agent pattern with shadow agent for planning.

    Equivalent to AutoGen's SingleAssistantShadow with nested chats.
    Shadow agent creates plan, main agent executes with tools.
    """

    def __init__(
        self,
        agent_config: str | Dict[str, Any],
        chat_client=None,
        toolkit_registry: Optional[Dict] = None,
        shadow_instructions: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize shadow workflow.

        Args:
            agent_config: Main agent name or configuration
            chat_client: Chat client instance
            toolkit_registry: Custom toolkit registry
            shadow_instructions: Custom instructions for shadow agent
            **kwargs: Additional arguments
        """
        super().__init__(agent_config, chat_client, toolkit_registry)

        # Create shadow agent (no tools, planning only)
        default_shadow_instructions = """
        You are a planning agent. Your role is to:
        1. Analyze the user's request
        2. Break it down into clear, actionable steps
        3. Determine what resources and tools are needed
        4. Create a detailed execution plan

        Provide a step-by-step plan that the execution agent can follow.
        """

        self.shadow_agent = ChatAgent(
            name=f"{self.agent.name}_Shadow",
            chat_client=chat_client,
            instructions=shadow_instructions or default_shadow_instructions,
            tools=None,  # Shadow has no tools
        )

        self.shadow_thread = self.shadow_agent.get_new_thread()

    async def chat(self, message: str, stream: bool = False, **kwargs):
        """
        Run dual-agent workflow.

        Args:
            message: User request
            stream: Whether to stream response
            **kwargs: Additional arguments

        Returns:
            AgentRunResponse with final result
        """
        # Step 1: Shadow agent creates plan
        plan_response = await self.shadow_agent.run(
            f"Create an execution plan for: {message}",
            thread=self.shadow_thread
        )

        plan = plan_response.text

        # Step 2: Main agent executes plan
        execution_message = f"""
Execute the following plan:

{plan}

Original request: {message}
"""

        if stream:
            return self.agent.run_stream(execution_message, thread=self.thread)
        else:
            response = await self.agent.run(execution_message, thread=self.thread)
            return response

    def reset(self):
        """Reset both main and shadow threads."""
        super().reset()
        self.shadow_thread = self.shadow_agent.get_new_thread()


class MultiAssistant(WorkflowBase):
    """
    Multi-agent group chat workflow.

    Equivalent to AutoGen's MultiAssistant with GroupChat.
    Multiple agents collaborate to solve tasks.
    """

    def __init__(
        self,
        agent_configs: List[str | Dict[str, Any]],
        chat_client=None,
        toolkit_registry: Optional[Dict] = None,
        max_rounds: int = 10,
        selector_func: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize multi-agent workflow.

        Args:
            agent_configs: List of agent names or configurations
            chat_client: Chat client instance
            toolkit_registry: Custom toolkit registry
            max_rounds: Maximum conversation rounds
            selector_func: Optional custom speaker selection function
            **kwargs: Additional arguments
        """
        # Initialize base without creating agent
        if chat_client is None:
            config = get_config()
            chat_client = config.get_chat_client()

        self.chat_client = chat_client

        if toolkit_registry is None:
            toolkit_registry = create_default_toolkit_registry()

        self.toolkit_registry = toolkit_registry

        # Create all agents
        self.agents = []
        for agent_config in agent_configs:
            if isinstance(agent_config, str):
                agent = create_agent(agent_config, chat_client, toolkit_registry)
            else:
                agent = create_agent(
                    agent_config.get("name", "CustomAgent"),
                    chat_client,
                    toolkit_registry
                )
            self.agents.append(agent)

        self.max_rounds = max_rounds
        self.selector_func = selector_func
        self.conversation_history = []

    async def chat(self, message: str, **kwargs):
        """
        Run multi-agent group chat.

        Note: This is a simplified implementation. For production use,
        consider using Agent Framework's GroupChatBuilder.

        Args:
            message: Initial user message
            **kwargs: Additional arguments

        Returns:
            Final response from group chat
        """
        from agent_framework import GroupChatBuilder

        # Build group chat workflow
        builder = GroupChatBuilder().participants(self.agents).with_max_rounds(self.max_rounds)

        if self.selector_func:
            builder = builder.set_custom_selector(self.selector_func)
        else:
            # Use default LLM-based selector
            builder = builder.set_prompt_based_manager(
                chat_client=self.chat_client,
                instructions="Select the most appropriate expert for the current task."
            )

        workflow = builder.build()

        # Run workflow
        result = await workflow.run(message)
        return result

    def reset(self):
        """Reset conversation history."""
        self.conversation_history = []


class MultiAssistantWithLeader(WorkflowBase):
    """
    Hierarchical multi-agent workflow with leader coordination.

    Equivalent to AutoGen's MultiAssistantWithLeader with nested chats.
    Leader agent delegates tasks to team members.
    """

    def __init__(
        self,
        leader_config: str | Dict[str, Any],
        team_configs: List[str | Dict[str, Any]],
        chat_client=None,
        toolkit_registry: Optional[Dict] = None,
        max_rounds: int = 10,
        **kwargs
    ):
        """
        Initialize hierarchical workflow.

        Args:
            leader_config: Leader agent name or configuration
            team_configs: List of team member agent configurations
            chat_client: Chat client instance
            toolkit_registry: Custom toolkit registry
            max_rounds: Maximum conversation rounds
            **kwargs: Additional arguments
        """
        # Initialize leader
        super().__init__(leader_config, chat_client, toolkit_registry)
        self.leader = self.agent

        # Create team members (use self.chat_client which was set by super().__init__)
        self.team = []
        for team_config in team_configs:
            if isinstance(team_config, str):
                agent = create_agent(team_config, self.chat_client, toolkit_registry)
            else:
                agent = create_agent(
                    team_config.get("name", "TeamMember"),
                    self.chat_client,
                    toolkit_registry
                )
            self.team.append(agent)

        self.max_rounds = max_rounds
        self.team_threads = {agent.name: agent.get_new_thread() for agent in self.team}

    async def chat(self, message: str, **kwargs):
        """
        Run hierarchical workflow.

        Note: This is a simplified implementation. For production use,
        consider using Agent Framework's WorkflowBuilder with custom executors.

        Args:
            message: Initial task description
            **kwargs: Additional arguments

        Returns:
            Final result from workflow
        """
        # Leader processes initial message
        leader_response = await self.leader.run(message, thread=self.thread)

        # Check if leader is delegating to team member
        # Format: "[Agent_Name] <instruction>"
        import re
        delegation_pattern = r'\[([^\]]+)\]\s*(.+)'
        match = re.search(delegation_pattern, leader_response.text)

        if match:
            team_member_name = match.group(1).strip()
            instruction = match.group(2).strip()

            # Find team member
            team_member = None
            for agent in self.team:
                if agent.name == team_member_name:
                    team_member = agent
                    break

            if team_member:
                # Execute delegation
                member_thread = self.team_threads[team_member_name]
                member_response = await team_member.run(instruction, thread=member_thread)

                # Send result back to leader
                feedback = f"Result from {team_member_name}: {member_response.text}"
                final_response = await self.leader.run(feedback, thread=self.thread)
                return final_response

        return leader_response

    def reset(self):
        """Reset all threads."""
        super().reset()
        self.team_threads = {agent.name: agent.get_new_thread() for agent in self.team}


# Convenience functions
def create_single_assistant(agent_name: str, **kwargs) -> SingleAssistant:
    """Create SingleAssistant workflow."""
    return SingleAssistant(agent_name, **kwargs)


def create_rag_assistant(agent_name: str, docs_path: str, **kwargs) -> SingleAssistantRAG:
    """Create RAG-enabled workflow."""
    return SingleAssistantRAG(agent_name, docs_path=docs_path, **kwargs)


def create_shadow_assistant(agent_name: str, **kwargs) -> SingleAssistantShadow:
    """Create shadow planning workflow."""
    return SingleAssistantShadow(agent_name, **kwargs)


def create_multi_assistant(agent_names: List[str], **kwargs) -> MultiAssistant:
    """Create multi-agent group chat."""
    return MultiAssistant(agent_names, **kwargs)


def create_leader_workflow(
    leader_name: str,
    team_names: List[str],
    **kwargs
) -> MultiAssistantWithLeader:
    """Create hierarchical leader-team workflow."""
    return MultiAssistantWithLeader(leader_name, team_names, **kwargs)
