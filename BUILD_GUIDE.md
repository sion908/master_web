# sion908 lab Blog 構築ガイド

Sphinxベースのモダンな技術ブログサイトの構築手順と設定をまとめたドキュメントです。

## 📋 概要

- **技術スタック**: Sphinx + Ablog + カスタムCSS
- **目的**: Qiita記事をベースにした技術ブログの静的サイト構築
- **特徴**: モダンなデザイン、紫苑色アクセント、レスポンシブ対応

## 🏗️ プロジェクト構成

```
sion908/
├── source/                    # Sphinxソースディレクトリ
│   ├── _static/              # 静的ファイル（CSSなど）
│   │   └── custom.css        # カスタムスタイルシート
│   ├── blog/                 # ブログ記事
│   │   ├── 2023/             # 年別ディレクトリ
│   │   ├── 2024/
│   │   ├── 2025/
│   │   └── 2026/
│   ├── index.rst             # トップページ
│   ├── blog.rst              # 記事一覧ページ
│   └── conf.py               # Sphinx設定
├── build/                    # ビルド出力ディレクトリ
├── pyproject.toml            # 依存関係
├── Makefile                  # ビルドコマンド
└── .venv/                    # Python仮想環境
```

## 🚀 構築手順

### 1. プロジェクト初期セットアップ

#### 1.1 仮想環境の作成と依存関係インストール

```bash
# Python仮想環境作成
python3 -m venv .venv

# 仮想環境有効化
source .venv/bin/activate

# 必要なパッケージインストール
pip install sphinx ablog sphinx-design sphinxemoji sphinxext-opengraph sphinx-nekochan pymdown-extensions
```

#### 1.2 pyproject.tomlの作成

```toml
[project]
name = "sion908-blog"
version = "0.1.0"
description = "Sion908's technical blog"
readme = "README.md"
authors = [{ name = "Sion908", email = "sionn908@gmail.com" }]
requires-python = ">=3.11"
dependencies = [
    "sphinx>=8.0.2",
    "ablog>=0.11.0",
    "sphinx-design>=0.6.1",
    "sphinxemoji>=0.3.1",
    "sphinxext-opengraph>=0.9.1",
    "sphinx-nekochan>=0.4.0",
    "pymdown-extensions>=10.0",
]

[tool.uv]
package = false
```

#### 1.3 ディレクトリ構造の作成

```bash
mkdir -p source/_static source/_templates source/blog/2024 source/blog/2025
```

### 2. Sphinxの設定

#### 2.1 conf.pyの作成

```python
# Configuration file for the Sphinx documentation builder.

project = 'Sion908 Blog'
copyright = '2026, sion908'
author = 'sion908'

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

html_theme = 'default'
html_static_path = ['_static']

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
```

### 3. カスタムデザインの実装

#### 3.1 custom.cssの作成

**ポイント**: CSS変数ベースのデザインシステムで、紫苑色（#867ba9）をアクセントカラーに採用

```css
/* CSS Variables */
:root {
    --primary-color: #867ba9;  /* 紫苑色 */
    --primary-dark: #6b5f8a;
    --primary-light: #a099bd;
    --secondary-color: #ec4899;
    --accent-color: #06b6d4;
    /* ... その他の変数 */
}

/* ダークモード対応 */
@media (prefers-color-scheme: dark) {
    :root {
        /* ダークモード用の色変数 */
    }
}

/* モダンなコンポーネントスタイル */
/* - ヘッダー、ナビゲーション */
/* - 記事カード、サイドバー */
/* - ボタン、タグ、フォーム */
/* - レスポンシブデザイン */
```

#### 3.2 デザインの特徴

- **カラーシステム**: CSS変数による一元管理
- **ダークモード**: OSの設定に応じた自動切り替え
- **タイポグラフィ**: モダンなフォントスタック
- **アニメーション**: 滑らかなトランジション効果
- **レスポンシブ**: モバイルファースト設計

### 4. 記事の移行と作成

#### 4.1 Qiita記事からSphinx形式への変換

**変換ルール**:
1. MarkdownからreStructuredTextへ変換
2. フロントマターをSphinxのpostディレクティブに変更
3. 画像パスの調整
4. コードブロックのシンタックス調整

**例: 変換前（Qiita Markdown）**
```markdown
---
title: 記事タイトル
tags:
  - Python
  - Flask
---

# 記事タイトル

本文...
```

**例: 変換後（Sphinx RST）**
```rst
記事タイトル
============

.. post:: 2025-03-16
   :tags: Python, Flask
   :author: sion908
   :language: ja
   :location: blog/2025

本文...
```

#### 4.2 移行した記事一覧

1. **AIペアプログラミングで体感する未来の開発** (2025-06-29)
2. **サーバを持たないSSR入門** (2025-12-18)
3. **PythonでORMを使わずSQL文で快適開発** (2025-11-12)
4. **AWS Lambdaとローカルで非同期処理** (2025-05-03)
5. **litestarのpolyfactoryでGeometryを扱う** (2025-03-23)
6. **python+sqlalchemy+lambdaで管理者画面を作る** (2024-12-20)
7. **gitのブランチ移動を簡単にする** (2023-11-15)
8. **FlaskでSQLSpecを使ったCRUDアプリ実装** (2026-03-16)

### 5. ページテンプレートの作成

#### 5.1 トップページ (index.rst)

**構成要素**:
- ヒーローセクション（サイト紹介）
- 最新記事表示（postlistディレクティブ）
- サイドバー（About Me、人気タグ、最近の活動）
- サイト間ナビゲーション

#### 5.2 記事一覧ページ (blog.rst)

**構成要素**:
- 全記事一覧表示
- タグ別フィルター機能
- ナビゲーションリンク

### 6. ビルドとデプロイ

#### 6.1 Makefileの作成

```makefile
# Makefile for Sphinx documentation
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets
html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "Build complete. The HTML pages are in $(BUILDDIR)/html."

clean:
	@rm -rf $(BUILDDIR)/*
	@echo "Cleaned build directory."

serve:
	@cd $(BUILDDIR)/html && python -m http.server 8080
	@echo "Server started at http://localhost:8080"

dev: html serve
	@echo "Development server started"
```

#### 6.2 ビルドコマンド

```bash
# HTMLサイトのビルド
make html

# ローカルサーバー起動
make serve

# 開発用（ビルド+サーバー起動）
make dev

# クリーンアップ
make clean
```

### 7. サイト間連携

#### 7.1 ナビゲーションリンク

- **ポートフォリオ**: `https://portfolio.sion908.tech/`
- **まめここ**: `https://www.mamekoko.sion908.tech/`
- **スライド**: `https://slide.sion908.tech/`
- **ブログ**: `https://sion908.tech/blog/`

#### 7.2 実装方法

```html
<div class="nav-links">
    <a href="https://portfolio.sion908.tech/" class="nav-link">
        <i class="fas fa-briefcase"></i>
        ポートフォリオ
    </a>
    <!-- 他のリンクも同様に -->
</div>
```

## 🎨 デザインシステム詳細

### カラーパレット

| 用途 | 色 | カラーコード | 説明 |
|------|----|------------|------|
| プライマリー | 紫苑色 | #867ba9 | メインアクセントカラー |
| プライマリー（ダーク） | | #6b5f8a | ホバー時など |
| プライマリー（ライト） | | #a099bd | 背景など |
| セカンダリー | ピンク | #ec4899 | 強調アクセント |
| アクセント | シアン | #06b6d4 | リンクなど |

### タイポグラフィ

```css
/* フントスタック */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 
             'Roboto', 'Helvetica Neue', Arial, 'Noto Sans', sans-serif;

/* 見出しサイズ */
h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
```

### コンポーネント

- **カード**: 角丸、シャドウ、ホバーエフェクト
- **ボタン**: グラデーション、変形アニメーション
- **ナビゲーション**: 背景ぼかし、境界線
- **サイドバー**: スティッキー配置、セクション分け

## 🔧 トラブルシューティング

### よくある問題と解決策

#### 1. ビルドエラー

**問題**: `externally-managed-environment` エラー
**解決策**: 仮想環境を使用する

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. CSSが反映されない

**問題**: カスタムCSSが適用されない
**解決策**: 
1. `html_static_path` と `html_css_files` の設定確認
2. ファイルパスの確認
3. ブラウザキャッシュのクリア

#### 3. 記事が表示されない

**問題**: postlistディレクティブで記事が表示されない
**解決策**:
1. 記事ファイルに `.. post::` ディレクティブがあるか確認
2. 日付形式が正しいか確認
3. ファイルの場所が正しいか確認

#### 4. 日本語が文字化けする

**問題**: 日本語が正しく表示されない
**解決策**:
1. `conf.py` に `language = 'ja'` を設定
2. ファイルのエンコーディングをUTF-8に確認

## 📝 今後の改善案

### 機能拡張

1. **検索機能**: Algoliaや自前検索の実装
2. **コメント機能**: Disqusや自前コメントシステム
3. **RSSフィード**: 詳細なフィード設定
4. **シンタックスハイライト**: Pygmentsのカスタマイズ
5. **ソーシャルシェア**: OGPタグの最適化

### デザイン改善

1. **マイクロインタラクション**: きめ細かなアニメーション
2. **ダークモード**: トグルボタンの追加
3. **印刷対応**: 印刷用スタイルの最適化
4. **アクセシビリティ**: キーボードナビゲーション、スクリーンリーダー対応

### パフォーマンス最適化

1. **画像最適化**: WebP形式、遅延読み込み
2. **CSS最適化**: 未使用スタイルの削除
3. **JavaScript最適化**: コード分割、遅延読み込み
4. **CDN対応**: 静的ファイルのCDN配信

## 📚 参考リンク

- [Sphinx公式ドキュメント](https://www.sphinx-doc.org/)
- [Ablog拡張](https://ablog.readthedocs.io/)
- [Sphinx Design](https://sphinx-design.readthedocs.io/)
- [CSS Variables](https://developer.mozilla.org/ja/docs/Web/CSS/Using_CSS_custom_properties)
- [レスポンシブデザイン](https://developer.mozilla.org/ja/docs/Learn/CSS/CSS_layout/Responsive_Design)

---

*このドキュメントはサイト構築の過程で得られた知見をまとめたものです。随時更新していきます。*
