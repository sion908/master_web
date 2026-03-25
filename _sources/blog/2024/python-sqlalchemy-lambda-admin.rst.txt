python+sqlalchemy+lambdaで管理者画面を作る
==========================================

.. post:: 2024-12-20
   :tags: Python, sqlalchemy, lambda, 管理者画面, sqladmin
   :author: sion908
   :language: ja
   :location: blog/2024

背景
----

バックエンドエンジニアをやっています。litestar+sqlalchemy+lambdaの構成でAPIをつくったのですが、フロントの方から管理者画面を作った方がいいよの声が...
普通みんな持ってるでしょって言われました
あるあるなんでしょうか？
みなさん教えてください

というわけで、管理者画面を拵えることになったのですが、工数はないので、適当なライブラリを使うことに。Djangoみたいに簡単にできればいいなというところで、`sqladmin <https://github.com/aminalaee/sqladmin>`_を見つけました。
簡単な管理者画面にはとてもいいのですが、jinja2で毎レスポンスごとに、全てのhtmlを送ってくる仕様でした。
ちょっと困るのでlambda+cognitoで使えるようにhtmxを使って書き換えることにしました。

TL;DR
-----

- sqladminでcrudできるの楽しい
- htmxおもしろい
- `sqladminlambda <https://github.com/sion908/sqladminlambda>`_作ってみたので、みてみてください

そもそも
--------

## sqladminについて

sqlalchemyのモデル定義をもとに、starlette系のASGIライブラリで管理者画面を作ることができる。
starletteでasgiを作り、sqlalchemyのモデルをwtformsでフォーム化、jinja2でhtmlをレンダリングする。

.. image:: https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/698479/4a83f763-444b-3acb-ff40-868dc1a9e270.png
   :width: 50%

.. image:: https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/698479/5bcb2a62-bd90-5d5e-c4ef-ab3e69a06b0d.png
   :width: 80%

## 利点
- 少しの変更で、crudができるようになる
- モデルのcrudの前に処理を挟むことができるので、必要な独自処理を追加できる
- 拡張性が高い

## 個人的に足りなかったこと
- 毎回全てのhtmlをレンダリングして返してくるので、効率が悪い
  - せめて、最小限のDOMを返すようにしたい
- cognitoに対応したい

開発
----

色々やってみたかったのですが、第一弾として、htmxに対応してもらって、id_tokenを渡すことで、apigatewayの認証にも対応できるようにしました。

やったこと
--------

- htmxによる擬似的なページ遷移の実現
- htmxによるDOM操作
- htmxでid_tokenを渡せるように修正

## htmxについて

.. code-block:: html

   <button hx-get="/api/user-info"
     hx-trigger="load"
     hx-headers='{"Authorization": "Bearer ${localStorage.getItem("id_token")}"}'
     hx-target="this"
     hx-push-url="true">
   </button>

このbutton操作によってできること

1. DOM操作
   - `hx-target`属性を使用して、更新する要素を指定
   - `hx-trigger`で、いつHTMXのリクエストを実行するかを制御

1. 認証トークンの設定
   - 個別のリクエストで`hx-headers`属性を使用してヘッダーを設定

1. ルーティングの仮想遷移
   - `hx-push-url="true"`属性により、ブラウザの履歴にURLを追加

終わりに
--------

あくまでも個人的見解です。
夢はあるなと
cognitoの対応もしたのですが、sqladminの外側で定義したので、ライブラリに含めることはできなかったです。
lambdaとsession周りをどう適応させるかわからず今回はこのような方式にしましたが、ちょくちょく認証が切れて、ログアウトさせられるのをどうにかしたいところです。
最近litestarにハマっているので、starlette系だけではなく、litestarにも対応させたいです。litestarの方にも`piccolo admin`がありましたが、こちらの方が使いやすそうな印象でした。
文章力がほしい...

参考
----

`https://aminalaee.dev/sqladmin/ <https://aminalaee.dev/sqladmin/>`_
