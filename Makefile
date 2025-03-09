.PHONY: clean-memory help

help: ## Display available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean-memory: ## Remove memory-bank directory
	@echo "Cleaning memory bank..."
	@if [ -d "memory-bank" ]; then \
		rm -rf memory-bank; \
		echo "✓ Memory bank directory removed"; \
	else \
		echo "! Memory bank directory not found"; \
	fi
