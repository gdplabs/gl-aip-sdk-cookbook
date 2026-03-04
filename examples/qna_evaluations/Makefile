.PHONY: install help

# Default target
install:
	@echo "� Checking prerequisites..."
	@command -v gcloud >/dev/null 2>&1 || { echo "❌ gcloud CLI not found."; echo "   Install from: https://cloud.google.com/sdk/docs/install"; exit 1; }
	@gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q . || { echo "❌ Not authenticated with gcloud."; echo "   Run: gcloud auth login"; exit 1; }
	@echo "✅ Prerequisites met"
	@echo "�📦 Installing dependencies via poetry..."
	poetry config http-basic.gen-ai oauth2accesstoken "$$(gcloud auth print-access-token)"
	poetry config http-basic.gen-ai-internal oauth2accesstoken "$$(gcloud auth print-access-token)"
	poetry config http-basic.gen-ai-publication oauth2accesstoken "$$(gcloud auth print-access-token)"
	poetry config http-basic.gen-ai-internal-publication oauth2accesstoken "$$(gcloud auth print-access-token)"
	poetry install --all-extras
	@echo "✅ Dependencies installed successfully"

help:
	@echo "Available targets:"
	@echo "  make install              - Install all dependencies via poetry"
	@echo "  make help                 - Show this help message"
