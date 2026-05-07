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

XML sitemap生成。SEOやクローラー向け。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/sitemap

**neighbors**

前後記事リンク（「前の記事」「次の記事」）。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/neighbors

**related-posts**

関連記事生成。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/related_posts

**series**

記事シリーズ化。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/series

Markdown / 執筆支援
~~~~~~~~~~~~~~~~~~

**liquid_tags**

有名プラグイン。YouTube、Vimeo、notebook、embedに対応。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/liquid_tags

使用例:

.. code-block:: jinja

   {% youtube xxxxx %}

**code_include**

外部コード埋め込み。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/code_include

使用例:

.. code-block:: jinja

   {% include_code app.py %}

**pelican-toc**

Table of Contents自動生成。

- GitHub: https://github.com/ingwinlu/pelican-toc

**better_code_samples**

コードブロック改善。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/better_code_samples

フロント最適化
~~~~~~~~~~~~

**webassets**

重要プラグイン。CSS minify、JS minify、Sass、Less、fingerprint/hashに対応。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/assets
- webassets docs: https://webassets.readthedocs.io/

**minify**

HTML/CSS/JS圧縮。

- PyPI: https://pypi.org/project/pelican-minify/

**gzip_cache**

gzip事前生成。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/gzip_cache

UX / ブログ機能
~~~~~~~~~~~~~~

**summary**

記事summary自動生成。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/summary

**readtime**

「5 min read」表示。

- GitHub: https://github.com/pelican-plugins/readtime

**tag_cloud**

タグクラウド生成。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud

**share_post**

SNS共有リンク生成。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/share_post

画像 / メディア
~~~~~~~~~~~~

**photos**

画像ギャラリー。

- GitHub: https://github.com/pelican-plugins/photos

**thumbnailer**

サムネ自動生成。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/thumbnailer

**pelican_youtube**

YouTube embedding。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/youtube

**pelican_vimeo**

Vimeo embedding。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/vimeo

Notebook / データ分析
~~~~~~~~~~~~~~~~~~~~

**ipynb**

Jupyter Notebook対応。

- GitHub: https://github.com/danielfrg/pelican-ipynb

**asciidoc_reader**

AsciiDoc対応。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/asciidoc_reader

多言語
~~~~~

**i18n_subsites**

多言語サイト対応。

- GitHub: https://github.com/pelican-plugins/i18n_subsites

**backref_translate**

翻訳記事対応。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/backlink_translate

コメント / 外部連携
~~~~~~~~~~~~~~~~~

**pelican_comment_system**

静的サイト向けコメント。

- GitHub: https://github.com/pelican-plugins/comment-system

**github_activity**

GitHub activity表示。

- 旧プラグイン: https://github.com/getpelican/pelican-plugins/tree/master/github_activity

**gravatar**

Gravatar表示。

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
