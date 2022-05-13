# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Sphynx Setup ------------------------------------------------------------
# Credit for sphynx documentation setup help: https://github.com/JamesALeedham/Sphinx-Autosummary-Recursion

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys
from datetime import date
from pathlib import Path

root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_path))

package_path = root_path / "yfpy"
sys.path.insert(0, str(package_path))

test_path = root_path / "test"
sys.path.insert(0, str(test_path))

from VERSION import __version__  # noqa

# -- Project information -----------------------------------------------------

project = "YFPY"
# noinspection PyShadowingBuiltins
copyright = f"{date.today().year}, Wren J. R. (uberfastman)"
author = "Wren J. R. (uberfastman)"

# The short X.Y version.
version = __version__
# The full version, including alpha/beta/rc tags.
release = __version__

# -- General configuration ---------------------------------------------------

# The master toctree document.
# master_doc = 'readme'

suppress_warnings = [
    "toc.circular",
    "myst.header"
]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",  # autogenerate documentation from docstrings
    "sphinx.ext.napoleon",  # support google style docstrings
    "sphinx.ext.autosummary",  # recursively generate documentation from dynamic nested modules
    "sphinx.ext.intersphinx",  # link to external documentation (must also use sphinx generated docs: .inv file)
    "sphinx.ext.viewcode",  # add links to the Python source code for classes, functions etc.
    "sphinx_autodoc_typehints",  # automatically document param types (less noise in class signature)
    "sphinx_rtd_dark_mode",  # add toggleable dark mode to sphinx ReadTheDocs theme
    "myst_parser"  # markdown parsing
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [
    "_static",
]

# html_logo = "yfpy-logo.png"
html_logo = "yfpy-logo.svg"
# see https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html for html_theme_options details
html_theme_options = {
    # "analytics_id": "G-XXXXXXXXXX",  #  Provided by Google in your dashboard
    "analytics_anonymize_ip": False,
    "logo_only": True,
    "display_version": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
    "vcs_pageview_mode": "",
    # "style_nav_header_background": "white",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": -1,
    "includehidden": True,
    "titles_only": False
}

# see https://pygments.org/docs/styles/ for documentation on pygments styles
# see https://pygments.org/styles/ for available pygments styles
# pygments_style = "sphinx"  # default for sphinx docs when no pygments style is specified
# pygments_style = "gruvbox-dark"
pygments_style = "friendly"


def setup(app):
    app.add_css_file("custom.css")


# -- Extension configuration -------------------------------------------------

# configure sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

# configure sphinx.ext.autosummary & sphinx_autodoc_typehints
autosummary_generate = True  # activate sphinx.ext.autosummary
autoclass_content = "both"  # add __init__ documentation (params, attributes) to class summaries
html_show_sourcelink = False  # remove "view source code" from top of html pages
autodoc_inherit_docstrings = True  # inherit docstrings from base class if no docstring is supplied
set_type_checking_flag = True  # enable "expensive" imports for sphinx_autodoc_typehints
add_module_names = False  # remove the Python namespaces from class/method signatures

# configure myst_parser
myst_heading_anchors = 6
myst_number_code_blocks = [
    # "shell",
    "python"
]
