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
ogp_description_length = 200  # 本文からの抽出文字数（:og:description:がある場合は無視されるはず）
ogp_social_cards = {
    "enable": True,
    "image_mini": "./_static/sion_rounded.png", # 右下のデフォルトロゴ(目)を独自の画像(角丸)に置き換え
    "font": "Hiragino Sans", # macOS内蔵の日本語フォントを指定
    "line_color": "#968ABD", # アクセントラインの色
    "description_max_length": 160, # 説明文の最大文字数（はみ出し防止）
    "page_title_max_length": 60, # ページタイトルの最大文字数（はみ出し防止）
}

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

# --- Monkey Patch for sphinxext-opengraph ---
# OGPソーシャルカード（PNG画像）と og:description のテキストを
# 本文ではなく .. meta:: :description: から取得するように差し替える。
# __init__.py は起動時に `from ._description_parser import get_description` で
# ローカル変数に束縛するため、モジュール側だけでなく __init__ 側も差し替える。
import docutils.nodes
import sphinxext.opengraph._description_parser as ogp_desc
import sphinxext.opengraph as ogp_init

original_get_desc = ogp_desc.get_description

def custom_get_description(doctree, length, known_titles):
    # .. meta:: ディレクティブの description を優先的に取得
    for node in doctree.traverse(docutils.nodes.meta):
        if node.get('name') == 'description':
            return node.get('content')
    # なければ元の挙動（本文からの抽出）にフォールバック
    return original_get_desc(doctree, length, known_titles)

# モジュールの参照とその利用元の両方を置き換える
ogp_desc.get_description = custom_get_description
ogp_init.get_description = custom_get_description
