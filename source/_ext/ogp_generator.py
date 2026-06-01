"""Sphinx用OGP画像生成拡張。

PILを使用してタイトルを折り返してOGP画像を生成する。
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util import logging
from ablog.blog import Blog

logger = logging.getLogger(__name__)


def _wrap_text(text: str, font, max_width: int, draw) -> list:
    """テキストを指定幅で折り返す。英単語の途中で改行しない。カッコと引用符を含めた単語を1つの単位として扱う。"""
    lines = []
    current_line = ""
    current_word = ""
    in_special = False  # カッコまたは引用符内
    
    for char in text:
        # 特殊文字の処理
        if char in ["（", "「"]:
            in_special = True
            # カッコの前の単語と結合
            if current_word:
                current_word += char
            elif current_line:
                # current_line全体をcurrent_wordに移動してカッコを追加
                current_word = current_line + char
                current_line = ""
            else:
                current_word = char
        elif char in ["）", "」"]:
            in_special = False
            current_word += char
        # 特殊文字内はすべて1つの単位として扱う
        elif in_special:
            current_word += char
        # 英単語の判定
        elif char.isascii() and not char.isspace():
            current_word += char
        else:
            # 単語が終了したら追加
            if current_word:
                test_line = current_line + current_word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                width = bbox[2] - bbox[0]
                
                if width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = current_word
                current_word = ""
            
            # 日本語やスペースを処理
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
    
    # 最後の単語を処理
    if current_word:
        test_line = current_line + current_word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = current_word
    
    if current_line:
        lines.append(current_line)
    
    return lines


def generate_ogp_image(app: Sphinx, pagename: str, templatename: str, context: dict, doctree: nodes.document) -> None:
    """各ページのOGP画像を生成する。"""
    logger.info(f"OGP生成チェック: pagename={pagename}, title={context.get('title', '')}")
    
    # ページタイトルを取得
    title = context.get("title", "")
    if not title:
        return
    
    # ブログ記事ページのみ対象（タグページやアーカイブページは除外）
    if not pagename.startswith("blog/"):
        logger.info(f"ブログ記事ではないためスキップ: {pagename}")
        return
    
    # タグページやアーカイブページを除外
    if "/tag/" in pagename or "/author/" in pagename or "/category/" in pagename or pagename in ["blog", "blog/drafts", "blog/archive"]:
        logger.info(f"タグ/アーカイブページのためスキップ: {pagename}")
        return
    
    # ベース画像のパス
    static_dir = Path(app.srcdir) / "_static"
    base_image_path = static_dir / "ogp_base.png"
    
    # ベース画像が存在しない場合は作成
    if not base_image_path.exists():
        # デフォルトのベース画像を作成（1200x630）
        base_img = Image.new("RGB", (1200, 630), (250, 250, 252))
        base_img.save(base_image_path)
        logger.info(f"ベース画像を作成しました: {base_image_path}")
    
    try:
        # ベース画像を読み込み
        base_img = Image.open(base_image_path).convert("RGBA")
        
        # テキスト描画用のオブジェクトを作成
        draw = ImageDraw.Draw(base_img)
        
        # フォント設定
        font_path = static_dir / "fonts" / "HackGen35-Regular.ttf"
        
        try:
            font = ImageFont.truetype(str(font_path), 48)
        except Exception:
            # フォントが見つからない場合はデフォルトフォントを使用
            font = ImageFont.load_default()
        
        # 画像サイズを取得
        img_width, img_height = base_img.size
        
        # マージン設定
        margin_left = 60
        margin_right = 60
        margin_top = 60
        margin_bottom = 60
        
        # タイトルエリアの設定
        title_start_y = margin_top
        max_text_width = img_width - margin_left - margin_right
        
        # テキストを折り返し
        lines = _wrap_text(title, font, max_text_width, draw)
        
        # 最大3行に制限
        if len(lines) > 3:
            lines = lines[:3]
            if len(lines[2]) > 10:
                lines[2] = lines[2][:9] + "..."
        
        # 各行の高さを計算
        line_height = 60
        total_text_height = len(lines) * line_height
        
        # タイトルを描画
        for i, line in enumerate(lines):
            y = title_start_y + i * line_height
            draw.text((margin_left, y), line, font=font, fill=(55, 65, 81))
        
        # 出力ディレクトリ
        output_dir = Path(app.outdir) / "_images" / "social_previews"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 出力ファイル名を生成
        output_filename = f"summary_{pagename.replace('/', '_')}.png"
        output_path = output_dir / output_filename
        
        # 画像を保存
        base_img.save(output_path, "PNG")
        logger.info(f"OGP画像を生成しました: {output_path}")
        
    except Exception as e:
        logger.warning(f"OGP画像生成エラー: {e}")


def setup(app: Sphinx) -> dict:
    """拡張機能のセットアップ。"""
    logger.info("OGP拡張: セットアップ開始")
    app.connect("html-page-context", generate_ogp_image)
    app.connect("blog-post-context", generate_ogp_image)
    app.connect("build-finished", lambda app, exc: logger.info("OGP拡張: build-finishedイベント発生"))
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
