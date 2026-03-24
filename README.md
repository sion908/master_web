# Sion908 Blog (Portal & Blog)

Sphinxベースのプレミアムなポータル・技術ブログサイトです。
グラスモーフィズム（Glassmorphism）を採用した独自のモダンデザインにより、個人ポータルとABlogによる技術発信を統合しています。

## ✨ 特徴

- 💎 **Premium Design**: グラスモーフィズム、動的グラデーション、洗練されたカードUIを採用
- 🎯 **Unified Layout**: `_templates/layout.html` によるサイト全体（ポータル・ブログ・法的ページ）の共通ヘッダー・フッター
- 🌸 **紫苑色テーマ**: 日本の伝統色「紫苑色（#867ba9）」を基調とした独自のアイデンティティ
- ⌨️ **HackGen Font**: 視認性の高いエンジニア向けフォント「HackGen」を標準採用
- 🚀 **SEO & Compliance**: `ads.txt`, `robots.txt`, `sitemap.xml` を自動生成に統合済み
- 📝 **ABlog Integration**: Sphinxによる高度な記事管理（タグ、アーカイブ、Atom/RSS）

## 🚀 クイックスタート

### 環境要件

- Python 3.11+
- pip

### セットアップ

```bash
# 1. リポジトリのクローン
git clone <repository-url>
cd sion908

# 2. 仮想環境の作成と有効化
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 3. 依存関係のインストール
pip install -r requirements.txt
# または直接
pip install sphinx ablog sphinx-design sphinxemoji sphinxext-opengraph sphinx-nekochan pymdown-extensions
```

### ビルドと実行

```bash
# サイトのビルド
make html

# ローカルサーバーでのプレビュー (デフォルト: 8000番ポート)
# build/html ディレクトリを任意のHTTPサーバーでホストしてください
# 例: python3 -m http.server 8000 -d build/html
```

## 📁 プロジェクト構成

```
sion908/
├── source/                  # Sphinxソース
│   ├── _static/             # 静的アセット
│   │   └── custom.css       # プレミアムデザインのコアスタイル
│   ├── _templates/          # カスタムテンプレート
│   │   └── layout.html      # サイト共通レイアウト (Header/Footer/Nav)
│   ├── _extra/              # ルート直下に配置されるSEOファイル
│   │   ├── ads.txt          # AdSense設定
│   │   ├── robots.txt       # クローラー設定
│   │   └── sitemap.xml      # サイトマップ
│   ├── blog/                # 記事データ (年別)
│   ├── index.rst            # ポータル（トップページ）
│   ├── blog.rst             # 記事一覧アーカイブ
│   ├── contact.rst          # お問い合わせ
│   ├── privacy.rst          # プライバシーポリシー
│   └── conf.py              # Sphinx/ABlog詳細設定
├── archive/                 # 旧型HTMLサイトのバックアップ
├── build/html/              # 生成された静的サイト（デプロイ対象）
├── .gitignore               # バージョン管理除外設定
└── README.md                # 本ファイル
```

## 📝 記事の追加・更新

1. `source/blog/YYYY/` ディレクトリに新しい `.rst` ファイルを作成
2. 以下のメタデータを含むテンプレートを使用してください：

```rst
記事タイトル
============

.. post:: 2026-03-25
   :tags: Python, AWS
   :author: sion908

ここに本文を書きます...
```

3. `make html` でビルドを実行し、`build/html/` 配下のファイルが更新されたことを確認します。

## 🎨 カスタマイズ

- **デザインの変更**: 全てのスタイルは `source/_static/custom.css` で管理されています。CSS変数（`:root`）を変更することで、ベースカラーやグラスモーフィズムの強度を調整できます。
- **ナビゲーション**: ヘッダーのリンクやフッターの構成は `source/_templates/layout.html` を直接編集してください。

## 📄 ライセンス

MIT License

---

Built with ❤️ by [sion908](https://github.com/sion908)
