# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'virton'
copyright = '2025, phum'
author = 'phum'
release = '1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser', 
]
myst_enable_extensions = ["attrs_inline"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ko'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_permalinks_icon = '<span>#</span>'
html_favicon = "_static/favicon.png"
html_theme_options = {
    "logo": {
        # 밝은 테마/어두운 테마 각각 지정
        "image_light": "_static/logo.png",
        "image_dark": "_static/logo.png",
        # 선택: 로고 옆에 표시할 텍스트
        # "text": "Virton Docs",
    },
    # 필요시 다른 옵션들…
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

import os   # 기존주석 해제
import sys  # 기존주석 해제
sys.path.insert(0, os.path.abspath('.')) # 기존주석 해제
