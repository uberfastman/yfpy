# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Determine this makefile's path.
# Be sure to place this BEFORE `include` directives, if any.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: build docs docs_no_build open_local_docs pages test_build test_deploy deploy help Makefile

build: ## Build PyPI packages for distribution.
	cd ${HOME}/Projects/personal/yfpy; python setup.py sdist bdist_wheel

docs: build ## Remove stale sphinx documentation and recreate new sphinx documentation.
	@$(MAKE) -f $(THIS_FILE) clean
	@$(MAKE) -f $(THIS_FILE) html

docs_no_build: ## Remove stale sphinx documentation and recreate new sphinx documentation without building PyPI package.
	@$(MAKE) -f $(THIS_FILE) clean
	@$(MAKE) -f $(THIS_FILE) html

open_local_docs: ## Open generated sphinx documentation locally for testing.
	open build/html/index.html

pages: docs ## Copy new sphinx documentation to /docs directory for GitHub Pages.
	python scripts/update_docs_for_github_pages.py;

test_build: pages ## Check PyPI packages for issues.
	cd ${HOME}/Projects/personal/yfpy; twine check dist/*

test_deploy: pages ## Deploy PyPI packages to Test PyPI.
	cd ${HOME}/Projects/personal/yfpy; twine upload -r testpypi dist/*

deploy: pages ## Deploy PyPI packages to PyPI.
	cd ${HOME}/Projects/personal/yfpy; twine upload dist/*

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
