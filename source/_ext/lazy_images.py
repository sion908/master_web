"""Sphinx拡張: 全ての<img>タグにloading="lazy"を自動付与する。

ファーストビューの画像（ヒーロー画像等）はブラウザが自動的に
eager loadingにフォールバックするため、全付与で問題ない。
"""

from sphinx.application import Sphinx
from sphinx.writers.html5 import HTML5Translator


def visit_image_add_lazy(self: HTML5Translator, node) -> None:
    """imageノードの処理後にloading="lazy"を挿入する。"""
    # 元のvisit_imageを呼び出した後、出力されたHTMLを加工する
    pass


def add_lazy_loading(app: Sphinx, pagename: str, templatename: str,
                     context: dict, doctree) -> None:
    """html-page-contextイベントで出力HTMLの<img>にloading="lazy"を追加。"""
    pass


def process_html(app: Sphinx, exception: Exception | None) -> None:
    """build-finishedイベントで全HTMLファイルの<img>にloading="lazy"を追加。"""
    import re
    from pathlib import Path

    if exception:
        return

    outdir = Path(app.outdir)
    img_pattern = re.compile(r'<img(?![^>]*loading=)([^>]*?)(/?)>', re.IGNORECASE)

    for html_file in outdir.rglob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        new_content = img_pattern.sub(r'<img loading="lazy"\1\2>', content)
        if new_content != content:
            html_file.write_text(new_content, encoding='utf-8')


def setup(app: Sphinx) -> dict:
    app.connect('build-finished', process_html)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
