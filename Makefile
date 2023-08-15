.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8 lint/black
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

run: ## Run the application
	@python -m gpt4docs gpt4docs

run-build: ## Run the application and without building the vectorstore
	@python -m gpt4docs gpt4docs --no-build

run-compile: ## Run the application and build the vectorstore
	@python -m gpt4docs gpt4docs --compile

run-readme:  ## Only run the readme
	@python -m gpt4docs gpt4docs --readme --no-docstring

init: ## Initialize environment variables
	@echo "Initializing environment variables...";
	@read -p "Please enter the Open AI API key: " key; \
	echo "OPENAI_API_KEY=$$key" > .env; \

install: ## Install the project for development
	@pip install poetry
	@poetry install
	@make init

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

test: ## run tests quickly with the default Python
	pytest

coverage: ## check code coverage quickly with the default Python
	coverage run --source gpt4docs -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html
