.PHONY: install install-dev lint test eval noise gate report clean help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install evalgate in production mode
	pip install -e .

install-dev: ## Install evalgate with dev dependencies
	pip install -e ".[dev]"
	pre-commit install

lint: ## Run linting (ruff check + ruff format check)
	ruff check evalgate/ tests/
	ruff format --check evalgate/ tests/

format: ## Auto-format code
	ruff check --fix evalgate/ tests/
	ruff format evalgate/ tests/

test: ## Run unit tests
	pytest tests/unit/ -v --tb=short

test-cov: ## Run tests with coverage report
	pytest tests/unit/ -v --tb=short --cov=evalgate --cov-report=term-missing

eval: ## Run full evaluation against the target RAG app
	evalgate run --config config.yaml

noise: ## Repeat baseline N times to measure run-to-run noise
	evalgate noise --repeats 5 --config config.yaml

gate: ## Run the regression gate (exit code 0 = pass, 1 = fail)
	evalgate gate --baseline runs/baseline.json --candidate runs/candidate.json

report: ## Generate HTML/Markdown evaluation report
	evalgate report --run-dir runs/latest/

clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
