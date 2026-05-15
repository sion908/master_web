PythonでORMを使わずSQL文で快適開発 - SQLSpecによるマイグレーション&CRUD実装
===============================================================================

.. post:: 2025-11-12
   :tags: Python, ORM, litestar, sqlspec, SQLite
   :author: sion908
   :language: ja
   :location: blog/2025

.. meta::
   :description: ORMの課題を解決するSQLSpecを使って、生SQLを書きながらも型安全性とマイグレーション管理を実現する方法を解説。

はじめに - ORMの課題とSQLSpecとの出会い
----------------------------------------

Webアプリケーション開発において、ORMは便利なツールですが、以下のような課題に直面することがあります：

- **複雑なクエリが書きにくい** - JOINや集計処理が多いと、ORM特有の記法が煩雑に
- **生SQLを結局書く** - パフォーマンスチューニングで生SQLに戻ることが多い
- **学習コストが高い** - SQLは知っているのに、ORM特有の記法を覚える必要がある

「SQLをそのまま書きたいけど、型安全性やマイグレーション管理は欲しい」

そんな中で見つけたのが **SQLSpec** というライブラリです。

.. warning::
   **注意**: SQLSpecは現在実験的なライブラリです。本番環境での使用前に十分な検証を行ってください。

SQLSpecとは
-----------

`SQLSpec <https://github.com/litestar-org/sqlspec>`_ は、SQL文をそのまま書きながら、以下の機能を提供するライブラリです：

- ✅ **Raw SQLをそのまま記述** - 学習コストが低い
- ✅ **型安全な結果マッピング** - Pydanticモデルへの自動変換
- ✅ **マイグレーション管理** - CLIでマイグレーション実行可能
- ✅ **複数DBサポート** - SQLite, PostgreSQL, MySQL等に対応
- ✅ **非同期対応** - aiosqlite, asyncpgなどをサポート

今回は **Litestar** (FastAPI類似のWebフレームワーク) + **SQLite** + **SQLSpec** でTODOアプリのCRUDとマイグレーションを実装してみます。

サンプルリポジトリ
------------------

完成したコードはこちら：

`https://github.com/sion908/litestar-sqlspec-app <https://github.com/sion908/litestar-sqlspec-app>`_

プロジェクト構成
----------------

.. code-block:: text

   litestar-sqlspec-app/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py           # Litestarアプリのエントリーポイント
   │   ├── db.py             # DB設定
   │   ├── models.py         # Pydanticモデル
   │   ├── routes.py         # APIルート
   │   └── migrations/       # マイグレーションファイル（手動作成）
   │       ├── 20251111125634_init.sql
   │       └── ...
   ├── pyproject.toml
   └── README.md

セットアップ
------------

1. 依存関係のインストール
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: toml

   # pyproject.toml
   [tool.poetry.dependencies]
   python = "^3.12"
   litestar = {extras = ["standard"], version = "^2.14.0"}
   sqlspec = {path = "sqlspec", develop = true, extras = ["aiosqlite"]}
   aiosqlite = "^0.20.0"
   pydantic = "^2.10.3"

.. code-block:: bash

   poetry install

2. データベース設定
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # app/db.py
   from pathlib import Path
   from sqlspec.adapters.aiosqlite import AiosqliteConfig

   def get_aiosqlite_config() -> AiosqliteConfig:
       db_path = Path("./data/app.db")
       db_path.parent.mkdir(parents=True, exist_ok=True)
       
       return AiosqliteConfig(
           pool_config={"database": str(db_path)},
           migration_config={
               "script_location": str(Path(__file__).parent / "migrations"),
               "version_table_name": "sqlspec_version",
           }
       )

3. Pydanticモデル定義
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # app/models.py
   from datetime import datetime
   from enum import Enum
   from typing import Optional
   from pydantic import BaseModel, Field, ConfigDict

   class Priority(str, Enum):
       LOW = "low"
       MEDIUM = "medium"
       HIGH = "high"

   class TaskBase(BaseModel):
       title: str = Field(..., min_length=1, max_length=200)
       description: Optional[str] = None
       completed: bool = False
       priority: Priority = Priority.MEDIUM
       due_date: Optional[datetime] = None

   class TaskCreate(TaskBase):
       pass

   class TaskUpdate(BaseModel):
       title: Optional[str] = Field(None, min_length=1, max_length=200)
       description: Optional[str] = None
       completed: Optional[bool] = None
       priority: Optional[Priority] = None
       due_date: Optional[datetime] = None

   class Task(TaskBase):
       model_config = ConfigDict(from_attributes=True)
       
       id: int
       created_at: datetime
       updated_at: datetime

マイグレーション管理
--------------------

マイグレーションファイルの作成
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::
   **重要**: SQLSpecではマイグレーションファイルは**自動生成されません**。手動でSQLファイルを作成する必要があります。

.. code-block:: bash

   # pyproject.tomlに設定を記述
   [tool.sqlspec]
   config = "app.db.get_aiosqlite_config"

   # マイグレーション用のディレクトリとファイルを手動作成
   mkdir -p app/migrations
   touch app/migrations/20251111125634_init.sql

マイグレーションファイルの構造：

.. code-block:: sql

   -- app/migrations/20251111125634_init.sql

   -- name: migrate-20251111125634-up
   CREATE TABLE IF NOT EXISTS tasks (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title TEXT NOT NULL,
       description TEXT,
       completed BOOLEAN NOT NULL DEFAULT 0,
       priority TEXT NOT NULL DEFAULT 'medium',
       due_date TIMESTAMP,
       created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TRIGGER IF NOT EXISTS update_tasks_updated_at
   AFTER UPDATE ON tasks
   FOR EACH ROW
   BEGIN
       UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
   END;

   -- name: migrate-20251111125634-down
   DROP TRIGGER IF EXISTS update_tasks_updated_at;
   DROP TABLE IF EXISTS tasks;

マイグレーションの実行
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # 最新バージョンまで適用
   sqlspec upgrade

   # 1つ戻す
   sqlspec downgrade -1

   # 特定バージョンまで適用
   sqlspec upgrade 20251111125634

   # 現在のバージョン確認
   sqlspec current

CRUD実装
--------

Litestarアプリケーションのセットアップ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # app/main.py
   from litestar import Litestar
   from sqlspec import SQLSpec
   from sqlspec.extensions.litestar import SQLSpecPlugin

   from app.db import get_aiosqlite_config
   from app.routes import TaskController

   # SQLSpec設定を登録
   sqlspec_registry = SQLSpec()
   sqlspec_registry.register_config(get_aiosqlite_config())

   app = Litestar(
       route_handlers=[TaskController],
       plugins=[SQLSpecPlugin(sqlspec_registry=sqlspec_registry)],
   )

CRUD エンドポイント実装
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # app/routes.py
   from typing import List, Optional
   from litestar import Controller, get, post, put, delete
   from litestar.exceptions import NotFoundException
   from sqlspec.adapters.aiosqlite import AiosqliteDriver

   from models import Task, TaskCreate, TaskUpdate

   class TaskController(Controller):
       path = "/tasks"

       @get()
       async def list_tasks(
           self,
           db_session: "AiosqliteDriver",
           completed: Optional[bool] = None,
           limit: int = 10,
           offset: int = 0
       ) -> List[Task]:
           """タスク一覧取得（フィルタ・ページネーション対応）"""
           query = """
               SELECT id, title, description, completed, priority, 
                      due_date, created_at, updated_at 
               FROM tasks
           """
           params = []

           if completed is not None:
               query += " WHERE completed = ?"
               params.append(completed)

           query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
           params.extend([limit, offset])

           # パラメータは *params で展開して渡す
           result = await db_session.execute(query, *params)
           # schema_typeはexecuteではなく、結果オブジェクトのメソッドで指定
           return result.get_data(schema_type=Task)

       @post()
       async def create_task(
           self,
           data: TaskCreate,
           db_session: "AiosqliteDriver",
       ) -> Task:
           """タスク作成"""
           task = await db_session.select_one(
               """
               INSERT INTO tasks (title, description, completed, priority, due_date)
               VALUES (?, ?, ?, ?, ?)
               RETURNING id, title, description, completed, priority, 
                         due_date, created_at, updated_at
               """,
               data.title,
               data.description or "",
               data.completed,
               data.priority,
               data.due_date,
               schema_type=Task
           )
           await db_session.commit()
           return task

       @get("/{task_id:int}")
       async def get_task(
           self,
           task_id: int,
           db_session: "AiosqliteDriver",
       ) -> Task:
           """タスク詳細取得"""
           task = await db_session.select_one_or_none(
               """
               SELECT id, title, description, completed, priority, 
                      due_date, created_at, updated_at
               FROM tasks
               WHERE id = ?
               """,
               task_id,
               schema_type=Task
           )
           if task is None:
               raise NotFoundException(f"Task with ID {task_id} not found")
           return task

       @put("/{task_id:int}")
       async def update_task(
           self,
           task_id: int,
           data: TaskUpdate,
           db_session: "AiosqliteDriver",
       ) -> Task:
           """タスク更新（部分更新対応）"""
           update_fields = []
           params = []

           if data.title is not None:
               update_fields.append("title = ?")
               params.append(data.title)
           if data.description is not None:
               update_fields.append("description = ?")
               params.append(data.description)
           if data.completed is not None:
               update_fields.append("completed = ?")
               params.append(data.completed)
           if data.priority is not None:
               update_fields.append("priority = ?")
               params.append(data.priority)
           if data.due_date is not None:
               update_fields.append("due_date = ?")
               params.append(data.due_date)

           if not update_fields:
               return await self.get_task(task_id, db_session)

           update_fields.append("updated_at = CURRENT_TIMESTAMP")
           params.append(task_id)

           query = f"""
               UPDATE tasks 
               SET {', '.join(update_fields)}
               WHERE id = ?
               RETURNING id, title, description, completed, priority,
                         due_date, created_at, updated_at
           """

           result = await db_session.execute(query, *params)
           task = result.one(schema_type=Task)
           await db_session.commit()
           return task

       @delete("/{task_id:int}", status_code=204)
       async def delete_task(
           self,
           task_id: int,
           db_session: "AiosqliteDriver",
       ) -> None:
           """タスク削除"""
           result = await db_session.execute(
               "DELETE FROM tasks WHERE id = ?",
               task_id
           )
           if result.rows_affected == 0:
               raise NotFoundException(f"Task with ID {task_id} not found")
           await db_session.commit()

SQLSpecの特徴的なポイント
-------------------------

1. パラメータの渡し方
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # ✅ execute()の場合: *params で展開して渡す
   result = await db_session.execute(query, *params)
   # schema_typeは結果オブジェクトで指定
   tasks = result.get_data(schema_type=Task)

   # ✅ select_one()やselect_one_or_none()の場合: schema_typeを直接指定可能
   task = await db_session.select_one(query, param1, param2, schema_type=Task)

   # 📝 Note: paramsはlistでもtupleでも問題なく動作します
   params = [10, 0]  # または params = (10, 0)
   result = await db_session.execute(query, *params)

2. 結果の型変換
^^^^^^^^^^^^^^^

SQLSpecは ``SQLResult`` オブジェクトを返し、以下のメソッドで型変換できます：

.. code-block:: python

   # 全件取得
   tasks = result.all(schema_type=Task)
   tasks = result.get_data(schema_type=Task)

   # 1件取得（0件または2件以上の場合はエラー）
   task = result.one(schema_type=Task)

   # 1件取得（0件の場合はNone）
   task = result.one_or_none(schema_type=Task)

   # 最初の1件（0件の場合はNone）
   task = result.get_first(schema_type=Task)

   # スカラー値（SELECT COUNT(*) などで使用）
   count = result.scalar()

   # 影響を受けた行数
   affected = result.rows_affected

3. トランザクション管理
^^^^^^^^^^^^^^^^^^^^^^^

Litestarの依存性注入により、``db_session`` が自動的にトランザクション管理されます：

.. code-block:: python

   # 変更を確定する場合は明示的にコミット
   await db_session.commit()

   # エラー時は自動的にロールバック
   # try-except不要（Litestarプラグインが自動処理）

動作確認
--------

.. code-block:: bash

   # マイグレーション実行
   sqlspec upgrade

   # サーバー起動
   litestar run --reload

   # APIテスト
   # タスク作成
   curl -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "買い物に行く", "priority": "high"}'

   # タスク一覧取得
   curl http://localhost:8000/tasks

   # 完了済みタスクのみ取得
   curl http://localhost:8000/tasks?completed=true

   # ページネーション
   curl http://localhost:8000/tasks?limit=5&offset=0

SQLSpec使用時の注意点
---------------------

マイグレーション
^^^^^^^^^^^^^^^^

- ❌ モデルからの自動生成は **サポートされていません**
- ✅ SQLファイルを手動で作成する必要があります
- ✅ タイムスタンプベースのファイル名を推奨（例: `20251111125634_init.sql`）
- ✅ `-- migrate-{version}-up` と `-- migrate-{version}-down` セクションの両方を記述

パラメータ処理
^^^^^^^^^^^^^^

- ✅ `execute()` では `*params` で展開
- ✅ `select_one()` では個別の引数として渡す
- ✅ listでもtupleでも動作します
- ⚠️ `execute()` に パラメータと共に`schema_type` を渡すとエラーになります

トランザクション
^^^^^^^^^^^^^^^^

- ✅ 変更系操作（INSERT/UPDATE/DELETE）後は `commit()` を呼ぶ
- ✅ SELECT のみの場合はcommit不要
- ✅ エラー時のロールバックは自動

まとめ
------

SQLSpecを使うことで、以下のメリットが得られました：

✅ **SQLをそのまま書ける** - ORMの学習コスト不要  
✅ **型安全** - Pydanticモデルへの自動マッピング  
✅ **マイグレーション管理** - CLIで簡単に実行  
✅ **柔軟性** - 複雑なクエリもそのまま記述可能  

一方で以下の点には注意が必要です：

⚠️ **実験的なライブラリ** - 本番環境では慎重に  
⚠️ **マイグレーションは手動** - SQLファイルを自分で書く必要がある  
⚠️ **ドキュメント不足** - 試行錯誤が必要な部分もある  

「ORMは便利だけど、結局SQL書くことが多い」という方で、実験的なツールを試してみたい方には、SQLSpecは興味深い選択肢になると思います。

完全なコードは `GitHubリポジトリ <https://github.com/sion908/litestar-sqlspec-app>`_ で公開していますので、ぜひ試してみてください！

参考リンク
----------

- `SQLSpec GitHub <https://github.com/litestar-org/sqlspec>`_
- `Litestar Documentation <https://docs.litestar.dev/>`_
- `Pydantic Documentation <https://docs.pydantic.dev/>`_
