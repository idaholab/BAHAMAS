# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../'))

project = 'BAHAMAS'
copyright = '2025, Congjian Wang, Tate H. Shorthill, Edward Chen, Jisuk Kim'
author = "Congjian Wang, Tate H. Shorthill, Edward Chen, Jisuk Kim"

release = '1.0.0'
# INL/RPT-25-88895
today = ''
today_fmt = '%B %d, %Y'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.intersphinx',
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
	'sphinx.ext.todo',
	"sphinx.ext.autodoc.typehints",
	"sphinx.ext.mathjax",
  "sphinx.ext.autosummary",
	"nbsphinx",  # <- For Jupyter Notebook support
	"sphinx.ext.napoleon",  # <- For Google style docstrings
	"sphinx.ext.viewcode",
	'autoapi.extension',
  'sphinx_copybutton',
  'sphinxcontrib.bibtex',
	# 'sphinx.ext.autosectionlabel',
	]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = [".rst", ".md"]
autoapi_dirs = ['../bahamas']

import sphinx_rtd_theme

html_theme = 'sphinx_rtd_theme'

# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# -- NBSphinx options
# Do not execute the notebooks when building the docs
nbsphinx_execute = "never"

autodoc_inherit_docstrings = False

# # -- Options for HTML output -------------------------------------------------
# # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_static_path = ['_static']

numfig = True
numfig_format = {
    'figure': 'Figure %s',
    'table': 'Table %s',
    'code-block': 'Listing %s',
}


# Optional: automatically number displayed math
math_number_all = True

# Optionally customize the format of equation numbers
math_eqref_format = "Eq. {number}"

bibtex_bibfiles = ['refs.bib']   # path(s) to your .bib file(s)
bibtex_default_style = 'unsrt'   # unsrt, plain, alpha, etc.

latex_engine = "xelatex"
latex_elements = {
    'printindex': r'\def\twocolumn[#1]{#1}\printindex',
    # "extraclassoptions": "landscape" # option to make it landscape to avoid line overflow
		'preamble': r'''
		\usepackage{titling}

		% Define custom fields
		\newcommand{\extratext}{Idaho National Laboratory}

		\usepackage{etoolbox}
		\makeatletter
		% Set starting page number
		\patchcmd{\pagemark}{\thepage}{\setcounter{page}{37}\thepage}{}{}
		\makeatother
		'''
}
