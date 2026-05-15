サーバを持たないSSR入門：Litestar + Jinja2 + MangumでLambdaに載せる
========================================================================

.. post:: 2025-12-18
   :tags: Python, jinja2, サーバーサイドレンダリング, Mangum, Litestar
   :author: sion908
   :language: ja
   :location: blog/2025

.. meta::
   :description: SSRの現代的な価値を見直し、Litestar+Jinja2+MangumでLambda上にサーバーレスSSR環境を構築した実践記録。

TL;DR
-----

- SSRは古いんじゃなくて、設計の節度を取り戻す技術だと思ってる
- Litestar + Jinja2 はSSRの"素直さ"が出る（テンプレ設定がまっすぐ）
- Lambda上では Mangum でASGIアプリをイベントに繋ぐのが手堅い
- htmxは"簡単に動く"けど、綺麗に育てる設計が意外と難しい（AIはそこに効く）

SSRが"当たり前じゃなくなった"今、なぜやるのか（思想）
------------------------------------------------------

ここ数年、Webは「まずSPA」がデフォになりました。体験は強い。けど個人開発だと、いつの間にか JSの依存・分業前提の設計・初期表示・SEOあたりがじわじわ重くなることがあります。

SSRは "最新トレンド" ではないかもしれない。でも僕はSSRを、懐古ではなく 「責務の境界を戻す」ための楔として見ています。

- まずHTMLが届く（＝まず見える）
- 画面の初期状態はサーバで決まる（＝状態の出どころが一つ）
- JSは必要な分だけ（＝保守が軽くなる）

SSRは「フロントの都合で世界を作る」より、「サーバが世界の骨格を握る」感じがして、精神衛生に良い。
（※もちろんサーバ側の負荷や複雑さが増えるトレードオフはある）

"Lambdaだけ"で済むのが正義（個人開発の速度感）
----------------------------------------------

SSRって「サーバを立てる」印象が強いけど、個人開発だとそこが心理的コストになります。

そこで AWS Lambda + API Gateway（または Function URL）。
サーバを持たずにSSRができると、体感として "始める重さ" が一段下がります。

LitestarはASGIアプリなので、Lambdaのイベント形式に橋渡しする必要があり、ここで Mangum が効きます。Mangumは ASGIアプリを Lambda 上で動かすためのアダプタで、API Gateway / Function URL などに対応しています。

Litestar + Jinja2：SSRの"素直さ"がある
---------------------------------------

Litestarはテンプレート機構を公式にサポートしていて、Jinja2も「普通に」組み込めます。

最小の雰囲気（超短縮）：

.. code-block:: python

   from pathlib import Path
   from litestar import Litestar, get
   from litestar.response import Template
   from litestar.contrib.jinja import JinjaTemplateEngine
   from litestar.template.config import TemplateConfig
   from mangum import Mangum

   @get("/")
   def index() -> Template:
       return Template("index.html.jinja2", {"msg": "SSR on Lambda"})

   app = Litestar(
       route_handlers=[index],
       template_config=TemplateConfig(
           directory=Path(__file__).parent / "templates",
           engine=JinjaTemplateEngine,
       ),
   )

   handler = Mangum(app)  # Lambda handler

ここまでで「LambdaのURLを叩いたらHTMLが返る」になります。
※静的ファイル配信は、S3+CloudFrontへ逃がすのが無難

htmxは"簡単に動く"けど"設計が効いてくる"
-----------------------------------------

SSRで十分に気持ちよくなるんですが、人間の欲望は尽きないので、次に欲しくなるのが部分更新。

htmxは hx-get でHTMLを取りにいって、DOMに差し替えられる。ここが軽い。
でも「運用できる設計」にする瞬間、急に難しくなります。

難しくなるポイント（体感）
- 境界問題：「どこを"部品"として返すか」が設計になる
- URL問題：フルページと部分HTMLのURLが増えがち
- 状態問題：サーバが持つ状態 / DOMの持つ状態がズレやすい
- 重複問題：全体テンプレと部分テンプレが二重管理になりやすい

htmxは"JSが減る"代わりに、テンプレ設計の精度が要求される感じがします。

じゃあAIは使えるのか？
-----------------------

使えます。ただし 「設計が未確定な状態」ではAIも迷子になることが多いです。
逆に、こちらが"型"を渡すと安定します。

AIが効く「型」

1) 命名規約を決めてから渡す

例：
- templates/pages/*.jinja2（フルページ）
- templates/partials/*.jinja2（差し替え用）

この規約があるだけで、AIに「partialはこれに従って」と言えます。

2) 「返していいHTMLの形」を決めてから渡す

例えば「/todos/partial は `<li>...</li>` の集合だけ返す。`<html>` は返さない」みたいに契約化。
hx-target で差し替え先が明確になるので、AIも実装しやすいです。

3) "部分レンダリング"の仕組みを用意しておく

Jinja2は普通に書くと「テンプレ丸ごと」レンダリングになりがちです。
ここで、テンプレのブロック単位をレンダリングできる jinja2-fragments みたいな道具があると、設計が少し楽になります（htmx文脈で「一部だけ返したい」に寄せられる）。

AIに「このブロックだけ返す設計で」と指定できるようになるのが大きい。

まとめ：SSRは"古い"んじゃなくて"節度"の技術
----------------------------------------------

LambdaだけでSSRを回せると、サーバ管理の気配が消えて、HTMLの素直さが前に出ます。
一方でhtmxは「簡単に動く」けど「綺麗に育つ」には設計がいる。だからこそAIは、コード生成より 境界・契約・命名規約を固める用途で効く…というのが現時点の結論です。

SPAが当たり前になった今だからこそ、SSRは回帰じゃなく、現代への楔として書く価値があると思っています。

参考文献
--------

- `Litestar Docs: Templating（Jinja2対応) <https://docs.litestar.dev/2/usage/templating.html>`_
- `Mangum: ASGI on AWS Lambda（概要） <https://github.com/Kludex/mangum>`_
- `htmx Docs: hx-get / hx-target <https://htmx.org/attributes/hx-get/>`_
