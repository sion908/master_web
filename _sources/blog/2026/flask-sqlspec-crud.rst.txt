FlaskでSQLSpecを使ったCRUDアプリ実装 - ORMを使わずに型安全なDB操作
======================================================================

.. post:: 2026-03-16
   :tags: Python, Flask, SQLite, sqlspec, CRUD
   :author: sion908
   :language: ja
   :location: blog/2026

はじめに
--------

FlaskでのDB操作といえばSQLAlchemyが定番ですが、生SQLを書きつつ型安全性も保ちたい場面があります。そんな時に出会ったのがSQLSpecです。

.. warning::
   注意: SQLSpecは現在実験的なライブラリです。本番環境での使用前に十分な検証を行ってください。

SQLSpecとは
-----------

`SQLSpec <https://github.com/litestar-org/sqlspec>`_ は生SQLを書きながら型安全なDB操作を可能にするライブラリ。ORM特有の記法を覚える必要がなく、SQL知識があればすぐに使えるのが特徴です。Flaskプラグインも提供されており、SQLite・PostgreSQL・MySQLなど複数のDBに対応しています。

プロジェクト構成
----------------

.. code-block:: text

   flask-sqlspec-demo/
   ├── app/
   │   ├── __init__.py         # Flaskアプリファクトリ
   │   ├── database.py         # DB初期化
   │   └── routes.py           # CRUDエンドポイント
   ├── data/                   # SQLite DBファイル用ディレクトリ
   ├── pyproject.toml
   ├── docker-compose.yml
   └── Dockerfile

サンプルレポジトリ
------------------

`https://github.com/sion908/sqlspec_flask <https://github.com/sion908/sqlspec_flask>`_

セットアップ
----------

### 1. 依存関係

.. code-block:: toml

   # pyproject.toml
   [project]
   name = "flask-sqlspec-demo"
   version = "0.1.0"
   description = "Flask + SQLSpec CRUD demo with SQLite"
   requires-python = ">=3.12"
   dependencies = [
       "flask>=3.0.0",
       "sqlspec[sqlite]>=0.1.0",
   ]

### 2. Docker環境

.. code-block:: dockerfile

   # Dockerfile
   FROM python:3.12-slim

   WORKDIR /app
   COPY pyproject.toml ./
   RUN pip install -e .

   COPY app/ ./app/

   EXPOSE 5000
   CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0"]

.. code-block:: yaml

   # docker-compose.yml
   services:
     app:
       build: .
       ports:
         - "5001:5000"
       volumes:
         - ./data:/data
       environment:
         - PYTHONDONTWRITEBYTECODE=1
         - PYTHONUNBUFFERED=1

実装
----

### 1. Flaskアプリファクトリ

.. code-block:: python

   # app/__init__.py
   from flask import Flask
   from sqlspec import SQLSpec
   from sqlspec.adapters.sqlite import SqliteConfig
   from sqlspec.extensions.flask import SQLSpecPlugin

   DB_PATH = "/data/app.db"

   sqlalchemy_spec: SQLSpec = SQLSpec()
   plugin: SQLSpecPlugin
   db_config: SqliteConfig

   def create_app() -> Flask:
       """Flask アプリを生成し、SQLSpec と CRUD Blueprintを登録する。"""
       global plugin, db_config

       app = Flask(__name__)

       # SQLSpec設定
       db_config = SqliteConfig(
           connection_config={"database": DB_PATH},
           extension_config={
               "flask": {
                   "commit_mode": "autocommit",
                   "session_key": "db",
               }
           },
       )
       sqlalchemy_spec.add_config(db_config)

       # Flaskプラグイン登録
       plugin = SQLSpecPlugin(sqlalchemy_spec, app)

       from app.database import init_db
       from app.routes import items_bp

       init_db(DB_PATH)
       app.register_blueprint(items_bp)

       return app

### 2. データベース初期化

.. code-block:: python

   # app/database.py
   import sqlite3

   CREATE_ITEMS_TABLE = """
   CREATE TABLE IF NOT EXISTS items (
       id          INTEGER PRIMARY KEY AUTOINCREMENT,
       name        TEXT    NOT NULL,
       description TEXT,
       created_at  TEXT    DEFAULT (datetime('now', 'localtime'))
   )
   """

   def init_db(db_path: str) -> None:
       """アプリ起動時に items テーブルを作成する。"""
       with sqlite3.connect(db_path) as conn:
           conn.execute(CREATE_ITEMS_TABLE)
           conn.commit()

### 3. CRUDエンドポイント

.. code-block:: python

   # app/routes.py
   from flask import Blueprint, jsonify, request
   from app import plugin

   items_bp = Blueprint("items", __name__, url_prefix="/items")

   @items_bp.get("/")
   def list_items():
       """全アイテムを取得する。"""
       db = plugin.get_session()
       rows = db.execute("SELECT id, name, description, created_at FROM items ORDER BY id")
       items = list(rows.all() if rows else [])
       return jsonify(items), 200

   @items_bp.post("/")
   def create_item():
       """新規アイテムを作成する。"""
       data = request.get_json(silent=True) or {}
       name = data.get("name", "").strip()
       if not name:
           return jsonify({"error": "nameは必須です"}), 400

       description = data.get("description")
       db = plugin.get_session()
       db.execute(
           "INSERT INTO items (name, description) VALUES (?, ?)",
           (name, description),
       )

       row = db.execute(
           "SELECT id, name, description, created_at FROM items WHERE rowid = last_insert_rowid()"
       )
       created = row.one()
       return jsonify(created), 201

   @items_bp.get("/<int:item_id>")
   def get_item(item_id: int):
       """指定IDのアイテムを取得する。"""
       db = plugin.get_session()
       row = db.execute(
           "SELECT id, name, description, created_at FROM items WHERE id = ?",
           (item_id,),
       )
       result = row.one_or_none()
       if result is None:
           return jsonify({"error": "アイテムが見つかりません"}), 404
       return jsonify(result), 200

   @items_bp.put("/<int:item_id>")
   def update_item(item_id: int):
       """指定IDのアイテムを更新する。"""
       db = plugin.get_session()

       existing = db.execute(
           "SELECT id FROM items WHERE id = ?", (item_id,)
       ).one_or_none()
       if existing is None:
           return jsonify({"error": "アイテムが見つかりません"}), 404

       data = request.get_json(silent=True) or {}
       name = data.get("name", "").strip()
       if not name:
           return jsonify({"error": "nameは必須です"}), 400

       description = data.get("description")
       db.execute(
           "UPDATE items SET name = ?, description = ? WHERE id = ?",
           (name, description, item_id),
       )

       row = db.execute(
           "SELECT id, name, description, created_at FROM items WHERE id = ?",
           (item_id,),
       )
       return jsonify(row.one()), 200

   @items_bp.delete("/<int:item_id>")
   def delete_item(item_id: int):
       """指定IDのアイテムを削除する。"""
       db = plugin.get_session()

       existing = db.execute(
           "SELECT id FROM items WHERE id = ?", (item_id,)
       ).one_or_none()
       if existing is None:
           return jsonify({"error": "アイテムが見つかりません"}), 404

       db.execute("DELETE FROM items WHERE id = ?", (item_id,))
       return jsonify({"message": f"アイテム {item_id} を削除しました"}), 200

SQLSpecの特徴的なポイント
--------------------------

### 1. Flask拡張の統合

SQLSpecのFlaskプラグインを使うことで、簡単にFlaskアプリに統合できます：

.. code-block:: python

   from sqlspec.extensions.flask import SQLSpecPlugin

   plugin = SQLSpecPlugin(sqlalchemy_spec, app)

   # エンドポイント内でセッション取得
   db = plugin.get_session()

### 2. 結果の操作

SQLSpecは `SQLResult` オブジェクトを返し、便利なメソッドを提供します：

.. code-block:: python

   # 全件取得
   rows = db.execute("SELECT * FROM items")
   items = list(rows.all() if rows else [])

   # 1件取得（必ず1件ある場合）
   item = row.one()

   # 1件取得（0件の場合はNone）
   item = row.one_or_none()

   # 影響を受けた行数
   affected = result.rows_affected

### 3. パラメータバインディング

SQLインジェクション対策のため、パラメータは必ずプレースホルダーを使用：

.. code-block:: python

   # ✅ 安全
   db.execute("SELECT * FROM items WHERE id = ?", (item_id,))

   # ❌ 危険
   db.execute(f"SELECT * FROM items WHERE id = {item_id}")

### 4. 自動コミットモード

Flask拡張の設定で `autocommit` モードを有効にできます：

.. code-block:: python

   extension_config={
       "flask": {
           "commit_mode": "autocommit",
           "session_key": "db",
       }
   }

これにより、明示的なコミットが不要になります。

動作確認
----------

### 1. アプリケーション起動

.. code-block:: bash

   # Dockerで起動
   docker-compose up --build

   # またはローカルで起動
   pip install -e .
   python -m flask --app app run --debug

### 2. APIテスト

.. code-block:: bash

   # アイテム作成
   curl -X POST http://localhost:5001/items \
     -H "Content-Type: application/json" \
     -d '{"name": "テストアイテム", "description": "これはテストです"}'

   # 全アイテム取得
   curl http://localhost:5001/items/

   # 特定アイテム取得
   curl http://localhost:5001/items/1

   # アイテム更新
   curl -X PUT http://localhost:5001/items/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "更新されたアイテム", "description": "更新されました"}'

   # アイテム削除
   curl -X DELETE http://localhost:5001/items/1

Flask + SQLSpecの利点
--------------------

### 1. シンプルさ

- 学習コストが低い - SQL知識があればすぐに使える
- コードが直感的 - ORM特有の記法を覚える必要がない
- デバッグが容易 - 実行されるSQLが明確

### 2. 柔軟性

- 複雑なクエリも対応 - JOIN、サブクエリなどもそのまま書ける
- DBに依存しない - SQLite、PostgreSQL、MySQLで同じ書き方
- パフォーマンス最適化 - SQLを直接制御できる

### 3. 型安全性

- 結果の型変換 - 自動で適切なPython型に変換
- エラーハンドリング - SQL実行時のエラーを適切に処理
- IDEサポート - SQLシンタックスハイライトが効く

注意点と制限
------------

### 1. 実験的なライブラリ

- 安定性 - API変更の可能性あり
- ドキュメント - まだ整備されていない部分あり
- コミュニティ - 小規模なため、情報が少ない

### 2. マイグレーション

- 自動生成なし - マイグレーションファイルは手動作成
- バージョン管理 - 別途管理が必要

### 3. Flask統合

- プラグイン依存 - Flask拡張に依存する部分あり
- セッション管理 - 複雑なトランザクションには工夫が必要

まとめ
------

Flask + SQLSpecで試してみた感想としては、ORMの学習コストをかけずに型安全なDB操作ができるのは魅力的でした。特にSQLを直接書ける点は、複雑なクエリが必要な場面で重宝しそうです。

ただし実験的なライブラリなので、本番利用は慎重に。マイグレーションも手動になるため、小規模なプロジェクトや個人開発向けかもしれません。

「ORMは便利だけど、もっとシンプルにSQLを書きたい」という場合は試す価値ありそうです。

コードは `GitHubリポジトリ <https://github.com/sion908/flask-sqlspec-demo>`_ に置いています。

参考リンク
---------

- `SQLSpec GitHub <https://github.com/litestar-org/sqlspec>`_
- `Flask Documentation <https://flask.palletsprojects.com/>`_
- `SQLite Documentation <https://sqlite.org/docs.html>`_
