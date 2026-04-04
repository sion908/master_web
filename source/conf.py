# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sion908 lab Blog'
copyright = '2026, sion908 lab'
author = 'sion908'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'ablog',
    'sphinx_design',
    'sphinxemoji.sphinxemoji',
    'sphinxext.opengraph',
    'sphinx_nekochan',
    'pymdownx.superfences',
    'pymdownx.highlight',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'default'
html_static_path = ['_static']
html_extra_path = ['_extra']

# Ablog configuration
blog_title = 'Sion908 Blog'
blog_baseurl = 'https://sion908.tech/blog'
blog_feed_fulltext = True
blog_feed_subtitle = 'Technical blog by Sion908'
blog_default_author = 'sion908'
blog_authors = {
    'sion908': ('https://sion908.tech', 'sionn908@gmail.com'),
}

# Font Awesome for icons
html_css_files = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
]

# Custom CSS
html_css_files.append('custom.css')

# OpenGraph configuration
ogp_site_url = 'https://sion908.tech'
ogp_description = 'Sion908の技術ブログ。Python、Web開発、クラウド技術などの記事を公開しています。'

# sphinx-nekochan フッター設定
nekochan_footer = {
    "text": "sion908.tech",
    "link": "https://sion908.tech",
    "target": "_blank",
}

# Post configuration (ablog)
fontawesome = {
    'github': 'fab fa-github',
    'twitter': 'fab fa-twitter',
    'linkedin': 'fab fa-linkedin',
}
