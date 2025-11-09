# FinRobot-AF Makefile
# Standardized commands for testing and development

PYTHON := /Users/admin/miniconda3/envs/finrobot/bin/python
TESTS_DIR := tests

.PHONY: help test test-unit test-integration test-tools test-e2e test-fast clean install

help:  ## Show this help message
	@echo "FinRobot-AF Development Commands"
	@echo "================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install FinRobot-AF in development mode
	$(PYTHON) -m pip install -e .

# Testing targets
test: ## Run all tests
	@echo "Running all tests..."
	$(PYTHON) $(TESTS_DIR)/unit/test_basic.py
	$(PYTHON) $(TESTS_DIR)/tools/test_tool_calling.py
	$(PYTHON) $(TESTS_DIR)/tools/test_real_api_calls.py
	$(PYTHON) $(TESTS_DIR)/integration/test_integration.py
	$(PYTHON) $(TESTS_DIR)/integration/test_multi_agent.py
	$(PYTHON) $(TESTS_DIR)/e2e/test_nvidia_analysis.py

test-unit:  ## Run unit tests only (fast, no API)
	@echo "Running unit tests..."
	$(PYTHON) $(TESTS_DIR)/unit/test_basic.py

test-tools:  ## Run tool verification tests
	@echo "Running tool tests..."
	$(PYTHON) $(TESTS_DIR)/tools/test_tool_calling.py
	$(PYTHON) $(TESTS_DIR)/tools/test_real_api_calls.py

test-integration:  ## Run integration tests (requires OpenAI API key)
	@echo "Running integration tests..."
	$(PYTHON) $(TESTS_DIR)/integration/test_integration.py
	$(PYTHON) $(TESTS_DIR)/integration/test_multi_agent.py

test-e2e:  ## Run end-to-end tests (complete scenarios)
	@echo "Running E2E tests..."
	$(PYTHON) $(TESTS_DIR)/e2e/test_nvidia_analysis.py

test-fast:  ## Run fast tests (unit + tools, no LLM calls)
	@echo "Running fast tests..."
	$(PYTHON) $(TESTS_DIR)/unit/test_basic.py
	$(PYTHON) $(TESTS_DIR)/tools/test_tool_calling.py
	$(PYTHON) $(TESTS_DIR)/tools/test_real_api_calls.py

# Cleanup
clean:  ## Clean up test artifacts and cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf build dist
	@echo "Cleaned up test artifacts"

# Quick commands
quick-test:  ## Quick verification (unit only)
	$(PYTHON) $(TESTS_DIR)/unit/test_basic.py

full-test:  ## Full test suite with reporting
	@make test
	@echo ""
	@echo "================================="
	@echo "All tests completed!"
	@echo "================================="
