.PHONY: help sync setup-auth install clean run pre-commit

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# UV binary path - try PATH first, then fallback to common locations
UV := $(shell command -v uv 2>/dev/null || echo "$(HOME)/.local/bin/uv")

# Private registries
REGISTRY_INTERNAL := https://us-central1-python.pkg.dev/gen-ai-internal-421607/gen-ai-internal/simple
REGISTRY_GEN_AI := https://us-central1-python.pkg.dev/gen-ai-internal-421607/gen-ai/simple

help: ## Show this help message
	@echo "$(BLUE)Hello World Local Agent - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup-auth: ## Setup authentication for private repositories
	@echo "$(BLUE)🔐 Setting up authentication for private repositories...$(NC)"
	@TOKEN=$$(gcloud auth print-access-token 2>/dev/null); \
	if [ -z "$$TOKEN" ]; then \
		echo "$(RED)✗ Failed to get gcloud token$(NC)"; \
		echo "  Run: gcloud auth login"; \
		exit 1; \
	fi; \
	export UV_INDEX_GEN_AI_USERNAME="oauth2accesstoken"; \
	export UV_INDEX_GEN_AI_PASSWORD="$$TOKEN"; \
	echo "$(GREEN)✓ Authentication configured$(NC)"; \
	echo "  UV_INDEX_GEN_AI_USERNAME=oauth2accesstoken"; \
	echo "  UV_INDEX_GEN_AI_PASSWORD=<token>"; \
	echo ""; \
	echo "$(YELLOW)Note: Run 'source <(make setup-auth)' to export variables$(NC)"

sync: ## Sync all dependencies including private packages
	@echo "$(BLUE)🔐 Getting Google Cloud access token...$(NC)"
	@TOKEN=$$(gcloud auth print-access-token 2>/dev/null); \
	if [ -z "$$TOKEN" ]; then \
		echo "$(RED)✗ Failed to get gcloud token$(NC)"; \
		echo "  Run: gcloud auth login"; \
		exit 1; \
	fi; \
	echo "$(GREEN)✓ Got access token$(NC)"; \
	echo ""; \
	echo "$(BLUE)📦 Syncing dependencies with UV...$(NC)"; \
	UV_PYTHON=python3.12 \
	UV_INDEX_GEN_AI_USERNAME=oauth2accesstoken \
	UV_INDEX_GEN_AI_PASSWORD="$$TOKEN" \
	UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken \
	UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$TOKEN" \
	$(UV) sync; \
	echo "$(GREEN)✓ All dependencies synced successfully!$(NC)"

install: sync ## Alias for sync

clean: ## Remove virtual environment and cache
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	@rm -rf .venv
	@rm -rf .uv_cache
	@rm -rf __pycache__
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

run: ## Run the local agent example
	@echo "$(BLUE)🚀 Running Hello World Local Agent...$(NC)"
	@$(UV) run python main.py

run-verbose: ## Run with verbose output
	@echo "$(BLUE)🚀 Running Hello World Local Agent (verbose)...$(NC)"
	@$(UV) run python main.py

pre-commit: ## Run pre-commit hooks
	@echo "$(BLUE)🔍 Running pre-commit hooks...$(NC)"
	@cd ../../../glaip-sdk && poetry run pre-commit run --files ../gl-agents/projects/multi-agent-system-patterns/**/*
	@echo "$(GREEN)✓ Pre-commit checks complete$(NC)"

.PHONY: help setup-auth sync install clean run run-verbose pre-commit
