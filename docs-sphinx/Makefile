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

.PHONY: build docs pages test_build test_deploy deploy help Makefile

build: ##
	cd ${HOME}/Projects/personal/yfpy; python setup.py sdist bdist_wheel

docs: build ## Remove stale sphinx documentation and recreate new sphinx documentation.
	@$(MAKE) -f $(THIS_FILE) clean
	@$(MAKE) -f $(THIS_FILE) html

pages: docs ## Copy new sphinx documentation to /docs directory for Github Pages.
	python scripts/update_docs_for_github_pages.py;

test_build: pages ##
	cd ${HOME}/Projects/personal/yfpy; twine check dist/*

test_deploy: pages ##
	cd ${HOME}/Projects/personal/yfpy; twine upload -r testpypi dist/*

deploy: pages ##
	cd ${HOME}/Projects/personal/yfpy; twine upload dist/*

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
