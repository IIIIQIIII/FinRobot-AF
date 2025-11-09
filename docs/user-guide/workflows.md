# Workflows User Guide

Master workflow orchestration patterns in FinRobot-AF for coordinating single and multi-agent systems.

## What are Workflows?

Workflows are orchestration patterns that define how agents interact, collaborate, and complete complex tasks. FinRobot-AF provides 5 pre-built workflow patterns:

1. **SingleAssistant** - Basic agent-user interaction
2. **SingleAssistantRAG** - Agent with document retrieval
3. **SingleAssistantShadow** - Dual-agent planning pattern
4. **MultiAssistant** - Group chat collaboration
5. **MultiAssistantWithLeader** - Hierarchical coordination

## Workflow Patterns

### 1. SingleAssistant

The simplest pattern: one agent with tool execution capabilities.

**Use When**:
- Simple queries and tasks
- Single-domain problems
- Quick data retrieval
- Straightforward analysis

**Example**:
```python
from finrobot.agents.workflows import SingleAssistant

# Create assistant
assistant = SingleAssistant("Market_Analyst")

# Execute task
response = await assistant.chat(
    "Get Apple (AAPL) stock price and calculate 50-day moving average"
)
print(response.text)
```

**Architecture**:
```
User → Agent → Tools → Response
```

**Configuration Options**:
```python
assistant = SingleAssistant(
    agent_config="Market_Analyst",  # Agent name or config dict
    chat_client=None,               # Optional custom chat client
    toolkit_registry=None,          # Optional custom tools
    max_turns=10                    # Maximum conversation turns
)
```

### 2. SingleAssistantRAG

Agent enhanced with retrieval-augmented generation (RAG) for document-based analysis.

**Use When**:
- Need to query internal documents
- Analyzing earnings reports
- Research with company filings
- Document-based Q&A

**Example**:
```python
from finrobot.agents.workflows import SingleAssistantRAG

# Create RAG-enabled assistant
assistant = SingleAssistantRAG(
    agent_config="Expert_Investor",
    docs_path="./financial_reports",      # Path to documents
    collection_name="earnings_q4_2024"    # ChromaDB collection
)

# Query with document context
response = await assistant.chat(
    "Based on Q4 earnings reports, what are key revenue trends across tech companies?"
)
print(response.text)
```

**Architecture**:
```
User → Query → Vector DB → Relevant Docs → Agent + Context → Response
```

**Document Setup**:
```python
# Documents are automatically loaded from docs_path
# Supported formats: .txt, .pdf, .md, .json

# File structure:
# ./financial_reports/
#   ├── apple_10k_2024.pdf
#   ├── msft_earnings_q4.txt
#   └── tech_sector_analysis.md
```

**Advanced Configuration**:
```python
assistant = SingleAssistantRAG(
    agent_config="Expert_Investor",
    docs_path="./reports",
    collection_name="my_collection",
    embedding_model="text-embedding-ada-002",  # Custom embeddings
    chunk_size=1000,                           # Document chunk size
    chunk_overlap=200,                         # Overlap between chunks
    k=5                                        # Number of docs to retrieve
)
```

### 3. SingleAssistantShadow

Dual-agent pattern: planner creates strategy, executor implements it.

**Use When**:
- Complex multi-step tasks
- Need explicit planning
- Long-form reports
- Structured analysis

**Example**:
```python
from finrobot.agents.workflows import SingleAssistantShadow

# Create shadow assistant
assistant = SingleAssistantShadow("Expert_Investor")

# Complex task requiring planning
response = await assistant.chat(
    "Create a comprehensive investment analysis for Tesla (TSLA): "
    "1) Financial health analysis "
    "2) Market position and competition "
    "3) Growth prospects "
    "4) Risk assessment "
    "5) Investment recommendation with price target"
)
print(response.text)
```

**Architecture**:
```
User → Planner → Plan → Executor → Tools → Response
       (Creates    ↓     (Implements
        strategy)         plan)
```

**How It Works**:
1. **Planner agent** receives task and creates detailed plan
2. **Plan** is reviewed and refined
3. **Executor agent** implements plan step-by-step
4. **Response** combines planning and execution

**Best Practices**:
```python
# Good: Complex, multi-step tasks
response = await shadow.chat(
    "Analyze Microsoft: fundamentals, technicals, valuation, and competitive position"
)

# Less effective: Simple queries (overhead not needed)
response = await shadow.chat("What is MSFT stock price?")
```

### 4. MultiAssistant

Group chat pattern where multiple specialized agents collaborate.

**Use When**:
- Need multiple perspectives
- Complex analysis requiring different expertise
- Cross-domain problems
- Comprehensive research

**Example**:
```python
from finrobot.agents.workflows import MultiAssistant

# Create team of agents
team = MultiAssistant([
    "Market_Analyst",      # Market data and trends
    "Financial_Analyst",   # Financial statements
    "Statistician"         # Risk analysis
])

# Collaborative task
response = await team.chat(
    "Analyze Netflix (NFLX) from three perspectives: "
    "market trends, financial health, and statistical risk profile"
)
print(response.text)
```

**Architecture**:
```
                    ┌─ Agent 1 (Market)
User → Coordinator → │─ Agent 2 (Financial) → Synthesis → Response
                    └─ Agent 3 (Statistics)
```

**Agent Interaction**:
- Agents take turns contributing
- Each sees previous contributions
- Collaborative problem-solving
- Round-robin or dynamic turn-taking

**Configuration**:
```python
team = MultiAssistant(
    agents_config=[
        "Market_Analyst",
        "Financial_Analyst",
        {"name": "Custom_Analyst", "instructions": "..."}  # Mix pre-configured and custom
    ],
    max_rounds=5,              # Maximum discussion rounds
    chat_client=None,          # Optional custom client
    toolkit_registry=None      # Optional custom tools
)
```

**Use Cases**:
```python
# Investment Committee
committee = MultiAssistant([
    "Expert_Investor",
    "Financial_Analyst",
    "Statistician"
])

# Due Diligence Team
due_diligence = MultiAssistant([
    "Financial_Analyst",
    "Market_Analyst",
    "Accountant"
])

# Research Team
researchers = MultiAssistant([
    "Data_Analyst",
    "Statistician",
    "Market_Analyst"
])
```

### 5. MultiAssistantWithLeader

Hierarchical pattern with leader coordinating team members.

**Use When**:
- Need structured delegation
- Leader should assign tasks
- Hierarchical workflow required
- Complex project coordination

**Example**:
```python
from finrobot.agents.workflows import MultiAssistantWithLeader

# Create hierarchical team
workflow = MultiAssistantWithLeader(
    leader_config="Financial_Analyst",    # Leader coordinates
    team_configs=[
        "Data_Analyst",                   # Team member 1
        "Statistician",                   # Team member 2
        "Market_Analyst"                  # Team member 3
    ]
)

# Leader delegates and synthesizes
response = await workflow.chat(
    "Perform complete financial analysis of Apple (AAPL): "
    "collect data, perform statistical analysis, and generate report"
)
print(response.text)
```

**Architecture**:
```
User → Leader → Delegates Tasks
         ↓
    Team Member 1 (executes)
    Team Member 2 (executes)
    Team Member 3 (executes)
         ↓
    Leader ← Synthesizes Results → Response
```

**Workflow Steps**:
1. **Leader** receives task
2. **Leader** creates plan and delegates
3. **Team members** execute assigned tasks
4. **Leader** synthesizes results
5. **Response** delivered to user

**Best Practices**:
```python
# Choose leader based on task
# For financial analysis: Financial_Analyst
# For investment strategy: Expert_Investor
# For data projects: Data_Analyst

workflow = MultiAssistantWithLeader(
    leader_config="Financial_Analyst",  # Financial focus
    team_configs=["Data_Analyst", "Statistician"],
    max_rounds=3
)
```

## Workflow Comparison

| Workflow | Agents | Planning | Complexity | Best For |
|----------|--------|----------|------------|----------|
| SingleAssistant | 1 | No | Low | Quick queries, simple tasks |
| SingleAssistantRAG | 1 | No | Medium | Document analysis, Q&A |
| SingleAssistantShadow | 2 | Yes | Medium | Complex reports, structured tasks |
| MultiAssistant | 2+ | Collaborative | High | Multiple perspectives, research |
| MultiAssistantWithLeader | 3+ | Hierarchical | High | Delegated tasks, projects |

## Choosing the Right Workflow

### Decision Tree

```
Is it a simple query or task?
├─ YES → SingleAssistant
└─ NO → Does it need document context?
    ├─ YES → SingleAssistantRAG
    └─ NO → Is explicit planning needed?
        ├─ YES → SingleAssistantShadow
        └─ NO → Need multiple perspectives?
            ├─ YES → Collaboration or delegation?
            │   ├─ Collaboration → MultiAssistant
            │   └─ Delegation → MultiAssistantWithLeader
            └─ NO → SingleAssistant
```

### Example Decision Making

**Task**: "Get AAPL stock price"
- **Decision**: SingleAssistant (simple, one agent sufficient)

**Task**: "Analyze earnings reports for trends"
- **Decision**: SingleAssistantRAG (needs document access)

**Task**: "Create comprehensive investment report"
- **Decision**: SingleAssistantShadow (complex, needs planning)

**Task**: "Analyze from market, financial, and risk perspectives"
- **Decision**: MultiAssistant (needs multiple expertise)

**Task**: "Coordinate team to research, analyze, and report"
- **Decision**: MultiAssistantWithLeader (hierarchical delegation)

## Common Workflow Patterns

### Pattern 1: Quick Analysis
```python
# Single agent for fast results
assistant = SingleAssistant("Market_Analyst")
response = await assistant.chat("Analyze TSLA recent performance")
```

### Pattern 2: Deep Research
```python
# RAG for document-based research
researcher = SingleAssistantRAG(
    "Expert_Investor",
    docs_path="./research_papers"
)
response = await researcher.chat(
    "Summarize key findings on EV market from research papers"
)
```

### Pattern 3: Comprehensive Report
```python
# Shadow for structured analysis
analyst = SingleAssistantShadow("Expert_Investor")
response = await analyst.chat(
    "Complete investment analysis: fundamentals, technicals, valuation"
)
```

### Pattern 4: Team Collaboration
```python
# Multi-agent for diverse insights
team = MultiAssistant([
    "Market_Analyst",
    "Financial_Analyst",
    "Statistician"
])
response = await team.chat(
    "Comprehensive NVDA analysis from all angles"
)
```

### Pattern 5: Delegated Project
```python
# Leader-based for coordinated work
project = MultiAssistantWithLeader(
    leader_config="Expert_Investor",
    team_configs=["Data_Analyst", "Market_Analyst", "Statistician"]
)
response = await project.chat(
    "Research semiconductor industry and identify top investment opportunities"
)
```

## Advanced Workflow Techniques

### Combining Workflows

Chain different workflows for complex pipelines:

```python
# Step 1: RAG for document research
rag_agent = SingleAssistantRAG("Expert_Investor", docs_path="./filings")
research = await rag_agent.chat("Extract key metrics from 10-K filings")

# Step 2: Multi-agent analysis
team = MultiAssistant(["Financial_Analyst", "Statistician"])
analysis = await team.chat(f"Analyze these metrics: {research.text}")

# Step 3: Shadow for final report
reporter = SingleAssistantShadow("Expert_Investor")
report = await reporter.chat(f"Create investment report based on: {analysis.text}")
```

### Custom Workflow State

Manage workflow state explicitly:

```python
class StatefulWorkflow:
    def __init__(self):
        self.assistant = SingleAssistant("Market_Analyst")
        self.results = []

    async def multi_step_analysis(self, symbols: list):
        for symbol in symbols:
            response = await self.assistant.chat(f"Analyze {symbol}")
            self.results.append({
                'symbol': symbol,
                'analysis': response.text
            })
            # Don't reset - maintain context
        return self.results

workflow = StatefulWorkflow()
results = await workflow.multi_step_analysis(['AAPL', 'MSFT', 'GOOGL'])
```

### Error Handling in Workflows

```python
async def robust_workflow(task: str):
    try:
        # Try complex workflow first
        team = MultiAssistant(["Market_Analyst", "Financial_Analyst"])
        response = await team.chat(task)
        return response.text
    except Exception as e:
        print(f"Multi-agent failed: {e}, falling back to single agent")
        # Fallback to simpler workflow
        agent = SingleAssistant("Market_Analyst")
        response = await agent.chat(task)
        return response.text

result = await robust_workflow("Analyze AAPL")
```

## Best Practices

### 1. Match Workflow to Task Complexity
- Don't use MultiAssistantWithLeader for simple queries
- Don't use SingleAssistant for tasks requiring multiple perspectives

### 2. Provide Clear Task Descriptions
```python
# Good: Specific and structured
response = await team.chat(
    "Analyze TSLA: "
    "1) Market Analyst: trend analysis "
    "2) Financial Analyst: balance sheet review "
    "3) Statistician: risk metrics"
)

# Less effective: Vague
response = await team.chat("Tell me about Tesla")
```

### 3. Reset State Between Unrelated Tasks
```python
# Analyze first company
await workflow.chat("Analyze AAPL")

# Reset before analyzing different company
workflow.reset()

# Analyze second company with fresh context
await workflow.chat("Analyze MSFT")
```

### 4. Monitor Resource Usage
```python
# MultiAssistant uses more tokens (multiple agents)
# Use for tasks that truly benefit from collaboration

# SingleAssistant more efficient for simple tasks
# Use when one perspective is sufficient
```

## Next Steps

- **[Agents Guide](agents.md)** - Learn about individual agents
- **[Tools Guide](tools.md)** - Understand available tools
- **[Tutorials](../tutorials/03-multi-agent-collaboration.md)** - Practice with workflows
- **[API Reference](../api/workflows.md)** - Detailed API documentation
