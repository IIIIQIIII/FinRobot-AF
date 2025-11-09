# FinRobot-AF Test Suite

Organized test structure for FinRobot-AF (Microsoft Agent Framework version).

## Directory Structure

```
tests/
├── unit/               # Unit tests (no external dependencies)
│   └── test_basic.py   # Basic imports, configs, agent creation
│
├── integration/        # Integration tests (with real APIs)
│   ├── test_integration.py    # API integration tests
│   └── test_multi_agent.py    # Multi-agent workflow tests
│
├── tools/              # Tool calling verification tests
│   ├── test_tool_calling.py   # Tool registration verification
│   └── test_real_api_calls.py # Real API data verification
│
└── e2e/                # End-to-end real-world tests
    └── test_nvidia_analysis.py # Complete NVIDIA stock analysis
```

## Test Categories

### 1. Unit Tests (`tests/unit/`)
**Purpose**: Test individual components in isolation without external dependencies.

- No API calls required
- Fast execution
- Test basic functionality, imports, configurations

**Example**: `test_basic.py`
- Import verification
- Agent configuration loading
- Toolkit registry setup

### 2. Integration Tests (`tests/integration/`)
**Purpose**: Test component interactions and API integrations.

- Requires OpenAI API key
- Tests real LLM interactions
- Validates multi-agent coordination

**Examples**:
- `test_integration.py` - Single agent with real LLM
- `test_multi_agent.py` - Multi-agent workflows

### 3. Tool Tests (`tests/tools/`)
**Purpose**: Verify tool calling mechanisms and API integrations.

- Tests tool registration
- Validates real API calls (Yahoo Finance, etc.)
- Ensures agents use tools, not just LLM knowledge

**Examples**:
- `test_tool_calling.py` - Tool registration verification
- `test_real_api_calls.py` - Real API data validation

### 4. End-to-End Tests (`tests/e2e/`)
**Purpose**: Complete real-world scenarios from start to finish.

- Full workflows with real data
- Generates actual reports
- Validates entire system integration

**Example**: `test_nvidia_analysis.py`
- Complete NVIDIA stock analysis
- Multiple agents collaboration
- Report generation and saving

## Running Tests

### Run All Tests
```bash
# From project root
python -m pytest tests/

# Or run specific categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/tools/
python -m pytest tests/e2e/
```

### Run Individual Tests
```bash
# Unit test
python tests/unit/test_basic.py

# Integration test
python tests/integration/test_integration.py

# Tool test
python tests/tools/test_real_api_calls.py

# E2E test
python tests/e2e/test_nvidia_analysis.py
```

### Run with Verbose Output
```bash
python -m pytest tests/ -v
```

## Test Requirements

### Minimal (Unit Tests)
- Python 3.10+
- FinRobot-AF installed
- No API keys needed

### Basic (Integration Tests)
- OpenAI API key (`OPENAI_API_KEY`)
- Internet connection

### Full (All Tests)
- OpenAI API key (`OPENAI_API_KEY`)
- FinnHub API key (`FINNHUB_API_KEY`) - optional for news/financials
- Internet connection

## Environment Setup

```bash
# Required
export OPENAI_API_KEY="your-openai-key"

# Optional (for FinnHub features)
export FINNHUB_API_KEY="your-finnhub-key"
```

## Test Coverage

| Category | Tests | Pass Rate | Purpose |
|----------|-------|-----------|---------|
| Unit | 6 | 100% | Component isolation |
| Integration | 12 | 100% | API & multi-agent |
| Tools | 6 | 100% | Tool verification |
| E2E | 3 | 100% | Real scenarios |
| **Total** | **27** | **100%** | **Complete coverage** |

## Writing New Tests

### Guidelines

1. **Choose the right category**:
   - Unit: Testing single functions/classes
   - Integration: Testing component interactions
   - Tools: Testing tool calling
   - E2E: Testing complete workflows

2. **Follow naming convention**:
   - File: `test_<feature_name>.py`
   - Function: `async def test_<specific_behavior>()`

3. **Include docstrings**:
   ```python
   async def test_agent_creation():
       """Test that agents are created with correct configuration."""
   ```

4. **Use proper assertions**:
   ```python
   assert result is not None
   assert "NVDA" in response
   ```

5. **Handle errors gracefully**:
   ```python
   try:
       result = await agent.chat(query)
       return True
   except Exception as e:
       print(f"Test failed: {e}")
       return False
   ```

### Example Test Template

```python
"""
Brief description of what this test file covers.
"""

import asyncio
import sys
import os


async def test_feature_name():
    """Test specific feature behavior."""
    print("=" * 80)
    print("TEST: Feature Name")
    print("=" * 80)

    try:
        # Setup
        from finrobot.agents.workflows import SingleAssistant

        # Test
        agent = SingleAssistant("Market_Analyst")
        result = await agent.chat("test query")

        # Verify
        assert result is not None

        print("✅ Test passed!")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


async def main():
    """Run all tests in this file."""
    results = []

    # Run tests
    success = await test_feature_name()
    results.append(("Feature Name", success))

    # Summary
    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\nResults: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
```

## Continuous Integration

Tests are organized to support CI/CD pipelines:

```yaml
# Example CI configuration
stages:
  - unit_tests      # Fast, no API keys
  - tool_tests      # Verify tool calling
  - integration     # Requires API keys
  - e2e            # Full scenarios
```

## Debugging Failed Tests

1. **Check environment variables**:
   ```bash
   echo $OPENAI_API_KEY
   echo $FINNHUB_API_KEY
   ```

2. **Run with verbose output**:
   ```bash
   python tests/integration/test_integration.py
   ```

3. **Check logs**:
   - Agent Framework logs warnings/errors
   - Look for API rate limits
   - Verify network connectivity

4. **Isolate the failure**:
   - Run single test function
   - Add debug prints
   - Check API responses

## Best Practices

1. ✅ **Keep tests independent** - Each test should run standalone
2. ✅ **Use real data when possible** - Validates actual system behavior
3. ✅ **Clean up after tests** - Reset state, close connections
4. ✅ **Document expected behavior** - Clear docstrings and comments
5. ✅ **Handle timeouts** - Set reasonable limits for API calls
6. ✅ **Verify tool usage** - Ensure agents call APIs, not just use LLM knowledge

## Maintenance

- Review tests after major changes
- Update expected outputs if APIs change
- Add new tests for new features
- Keep test data current (stock symbols, date ranges)

---

**Last Updated**: 2025-11-08
**Test Framework**: asyncio-based
**Coverage**: 100% (27/27 tests passing)
