# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'virton-documents'
copyright = '2025, FLORA'
author = 'FLORA'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser',
              'sphinx.ext.githubpages'
]
extensions.append("sphinx_wagtail_theme")

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_favicon='virton-favicon.ico'
html_logo='virton-logo.svg'



from recommonmark.parser import CommonMarkParser

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

html_baseurl="https://docs.virton.co.kr/build/html/"

import os   # 기존주석 해제
import sys  # 기존주석 해제
sys.path.insert(0, os.path.abspath('.')) # 기존주석 해제
