Pelicanプラグイン調査まとめ
=========================

.. post:: 2026-05-07
   :tags: Pelican, Python, 静的サイトジェネレーター, プラグイン, ブログ
   :author: sion908
   :language: ja
   :location: blog/2026

.. meta::
   :description: Pelicanプラグインの調査まとめ。プラグイン管理の歴史、代表的なプラグイン一覧、技術ブログ用途の最小構成、実運用方針、Pelican vs Nikolaの比較について解説します。

はじめに
--------

AI時代にPelicanを用いてGitHub Pagesとともに静的サイトの更新ができると思い、調査を始めました。

Pelicanのメンテナンスは少しゆっくりですが、一度使うためにプラグインをまとめておきたかったのがこの記事の動機です。

PelicanはPython製の静的サイトジェネレーターで、ブログ用途でよく使われています。

- 公式サイト: https://getpelican.com/
- GitHub: https://github.com/getpelican/pelican
- ドキュメント: https://docs.getpelican.com/
- PyPI: https://pypi.org/project/pelican/

プラグイン管理の歴史
--------------------

旧方式（monorepo）
~~~~~~~~~~~~~~~~~~

昔は以下の巨大リポジトリにプラグインがまとまっていました。

- https://github.com/getpelican/pelican-plugins

利用イメージ:

.. code-block:: python

   PLUGIN_PATHS = ["path/to/pelican-plugins"]
   PLUGINS = [
       "sitemap",
       "neighbors",
       "summary",
   ]

プラグインリポジトリをcloneし、必要なプラグインを有効化する方式でした。

現方式（namespace plugin）
~~~~~~~~~~~~~~~~~~~~~~~~~~~

現在はプラグインごとの個別リポジトリ管理へ移行中です。

- GitHub Organization: https://github.com/pelican-plugins

推奨利用方法:

.. code-block:: bash

   pip install pelican-sitemap

Pelican 4.5+ 以降はnamespace pluginの自動検出に対応しています。

参考: `Pelican 4.5 Release Notes <https://getpelican.com/blog/pelican-4.5-released/>`_

プラグイン探索の現状
--------------------

探す順番:

1. 公式Plugins docs
2. pelican-plugins organization
3. 旧 getpelican/pelican-plugins
4. PyPI classifier

- 公式Plugins docs: https://docs.getpelican.com/en/latest/plugins.html
- PyPI classifier: https://pypi.org/search/?c=Framework+%3A%3A+Pelican+%3A%3A+Plugins

代表的プラグイン一覧
------------------

SEO / サイト構造
~~~~~~~~~~~~~~~~

**sitemap**

XML sitemapを自動生成するプラグイン。検索エンジンのクローラーに対してサイトの構造や記事の更新頻度を適切に伝えるために必須のプラグインです。優先度（priority）や更新頻度（changefreq）の細かい設定も可能です。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/sitemap

**neighbors**

記事の末尾などに「前の記事」「次の記事」といったリンクを生成するための変数（ ``next_article`` / ``prev_article`` ）を提供します。読者の回遊率向上に役立ちます。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/neighbors

**related-posts**

記事のタグやカテゴリなどを解析し、関連する記事のリストを自動生成します。記事を読み終えた読者に次のコンテンツを提示し、サイトの直帰率を下げるのに効果的です。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/related_posts

**series**

複数の記事を「シリーズ」としてまとめる機能を提供します。連載記事やチュートリアルなどを書く際に、自動でシリーズ内の他の記事へのリンク一覧を出力してくれるため便利です。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/series

Markdown / 執筆支援
~~~~~~~~~~~~~~~~~~

**liquid_tags**

Jinjaのタグに似た記法で、YouTube動画、Vimeo、Jupyter Notebook、その他外部リソースを記事内に簡単に埋め込めるようにする非常に強力で多機能なプラグインです。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/liquid_tags

使用例:

.. code-block:: jinja

   {% youtube xxxxx %}

**code_include**

外部のソースコードファイルを指定して、その内容を記事内にインクルードする機能です。コードの断片をコピペせずに済むため、ソースコード自体を別ファイルとしてGitなどで管理・テストしやすくなります。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/code_include

使用例:

.. code-block:: jinja

   {% include_code app.py %}

**pelican-toc**

Markdownのヘッダー要素（h1, h2, h3など）から目次（Table of Contents）を抽出し、記事内の好きな場所やサイドバーに配置できるようにします。長文の技術記事には欠かせません。

- GitHub: https://github.com/ingwinlu/pelican-toc

**better_code_samples**

デフォルトのコードブロックのハイライトや行番号表示などの挙動を改善し、より見やすい技術記事を作成するためのプラグインです。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/better_code_samples

フロント最適化
~~~~~~~~~~~~

**webassets**

フロントエンドのビルドパイプラインをPelicanに統合する強力なプラグインです。CSS/JSのMinify、SassやLessのコンパイル、さらにはキャッシュバスティングのためのファイル名へのハッシュ付与（fingerprinting）まで対応します。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/assets
- webassets docs: https://webassets.readthedocs.io/

**minify**

ビルド出力されたHTML、CSS、JSファイルから不要な空白や改行を削除し、ファイルサイズを極限まで圧縮します。サイトの読み込み速度（パフォーマンス）を向上させるために有効です。

- PyPI: https://pypi.org/project/pelican-minify/

**gzip_cache**

ビルド時に、あらかじめgzip圧縮されたファイル（.html.gz、.css.gzなど）を生成しておくプラグインです。NginxなどのWebサーバー側の設定と組み合わせることで、動的圧縮のCPU負荷を下げつつ高速な配信が可能になります。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/gzip_cache

UX / ブログ機能
~~~~~~~~~~~~~~

**summary**

記事の冒頭部分や、指定した特定の区切り文字までの内容を抽出し、記事一覧ページなどで表示するための要約（サマリー）を自動生成します。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/summary

**readtime**

記事の文字数や単語数から「この記事を読むのにかかる時間（例: 5 min read）」を算出して表示します。Mediumなどのモダンなブログプラットフォームでよく見られる、読者の利便性を上げる機能です。

- GitHub: https://github.com/pelican-plugins/readtime

**tag_cloud**

サイト内で使用されているすべてのタグを集計し、使用頻度に応じた文字サイズで表示するタグクラウドを生成します。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud

**share_post**

Twitter（X）、Facebook、はてなブックマーク、LinkedInなどの各種SNS共有リンク（シェアボタン）用のURLを生成します。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/share_post

画像 / メディア
~~~~~~~~~~~~

**photos**

記事内に美しい画像ギャラリーを構築するためのプラグインです。複数の画像を綺麗に整列させて表示したい場合に使用します。

- GitHub: https://github.com/pelican-plugins/photos

**thumbnailer**

記事内で使用する元の大きな画像から、自動的に複数の指定サイズのサムネイル画像をビルド時に生成します。ページの読み込み速度最適化に役立ちます。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/thumbnailer

**pelican_youtube**

YouTube動画のURLやIDを指定するだけで、レスポンシブ対応（画面サイズに合わせて伸縮する）した動画プレイヤーを記事内に簡単に埋め込むことができます。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/youtube

**pelican_vimeo**

Vimeo動画の埋め込みを簡単に行うためのプラグインです。機能としては ``pelican_youtube`` のVimeo版に相当します。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/vimeo

Notebook / データ分析
~~~~~~~~~~~~~~~~~~~~

**ipynb**

Jupyter Notebookファイル（.ipynb）をそのままPelicanの記事としてビルドし、HTMLとしてレンダリングできるようにします。コードとその実行結果、グラフなどをそのままブログ化できるため、データサイエンティストなどに非常に人気があります。

- GitHub: https://github.com/danielfrg/pelican-ipynb

**asciidoc_reader**

MarkdownやreStructuredTextだけでなく、AsciiDoc形式で書かれたドキュメントをパースしてHTMLに変換するためのリーダープラグインです。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/asciidoc_reader

多言語
~~~~~

**i18n_subsites**

Pelicanで本格的な多言語サイト（例: 日本語版と英語版）を構築するための公式推奨プラグインです。言語ごとにサブサイトを生成し、言語間のリンクや設定の切り替えを管理します。

- GitHub: https://github.com/pelican-plugins/i18n_subsites

**backref_translate**

ある言語で書かれた記事に対して、別の言語の翻訳記事が存在する場合に、互いの記事へ相互リンクを自動的に張る機能を提供します。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/backlink_translate

コメント / 外部連携
~~~~~~~~~~~~~~~~~

**pelican_comment_system**

Disqusなどの外部サービスに依存せず、静的なファイル（Markdownなど）ベースでコメントシステムを構築するためのプラグインです。

- GitHub: https://github.com/pelican-plugins/comment-system

**github_activity**

指定したGitHubユーザーのアクティビティ（コミット、Issue作成、Pull Requestなど）をAPI経由で取得し、サイドバーなどにタイムラインとして表示します。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/github_activity

**gravatar**

メールアドレスからGravatarのプロフィール画像を取得し、著者情報などとともにアイコンとして表示するためのプラグインです。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/gravatar

技術ブログ用途の最小構成
----------------------

.. code-block:: python

   PLUGINS = [
       "sitemap",
       "neighbors",
       "summary",
       "related_posts",
       "pelican-toc",
   ]

必要に応じて追加:

- webassets
- ipynb
- series
- tipue_search

Plugin ecosystemの特徴
---------------------

良い点
~~~~~

- 歴史が長い
- プラグイン数が多い
- Pythonだけで完結しやすい

悪い点
~~~~~

- READMEが古いプラグインがある
- Python最新版未対応プラグインがある
- namespace plugin移行中
- メンテナンス停止プラグインが存在

実運用方針
----------

プラグインを大量導入しない方が安全です。

推奨:

- 5〜10プラグイン程度に絞る
- 定番プラグインのみ使う
- commit/activityを確認する

Pelican vs Nikola
----------------

Pelican
~~~~~~~

向いているケース:

- 普通の技術ブログ
- 軽量運用
- Markdown中心
- シンプル構成

Nikola
~~~~~~

向いているケース:

- Notebook
- 多言語
- ギャラリー
- データ分析ブログ

- 公式: https://getnikola.com/
- GitHub: https://github.com/getnikola/nikola

個人的な整理
------------

普通の技術ブログなら:

- Pelican
- Markdown
- GitHub Actions
- GitHub Pages / Cloudflare Pages

構成が最も軽いです。Notebook主体ならNikolaも検討価値あり。

参考リンク
----------

- `Pelican Official Site <https://getpelican.com/>`_
- `Pelican GitHub <https://github.com/getpelican/pelican>`_
- `Pelican Documentation <https://docs.getpelican.com/>`_
- `pelican-plugins Organization <https://github.com/pelican-plugins>`_
- `Old pelican-plugins Repository <https://github.com/getpelican/pelican-plugins>`_
- `Nikola <https://getnikola.com/>`_
