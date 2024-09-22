# You can set these variables from the command line and also from the environment.
DOCS_OPTS    ?=
DOCS_BUILD   ?= mkdocs

# Determine this makefile's path. Be sure to place this BEFORE `include` directives, if any.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

# Put it first so that "make" without argument is like "make help".
help:
	@$(DOCS_BUILD) -h $(DOCS_OPTS) $(O)

.PHONY: build verify_build test_docs docs pages test_deploy deploy help Makefile

build: ## Build PyPI packages for distribution.
	cd ${HOME}/Projects/personal/yfpy; python setup.py sdist bdist_wheel

verify_build: ## Check PyPI packages for issues.
	twine check dist/*

test_docs: ## Extract YFPY project version from VERSION.py and serve MkDocs documentation locally for testing.
	export YFPY_VERSION=$$(python -c "from VERSION import __version__; print(__version__)") && mkdocs serve

docs: build ## Extract YFPY project version from VERSION.py and build MkDocs documentation for distribution.
	export YFPY_VERSION=$$(python -c "from VERSION import __version__; print(__version__)") && mkdocs build

pages: docs ## Prepare documentation in /docs directory for GitHub Pages.
	python docs-mkdocs/scripts/update_docs_for_github_pages.py

test_deploy: pages ## Deploy PyPI packages to Test PyPI.
	twine upload -r testpypi dist/*

deploy: pages ## Deploy PyPI packages to PyPI.
	twine upload dist/*
