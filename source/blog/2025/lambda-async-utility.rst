AWS Lambdaとローカルで非同期処理をシームレスに実行するユーティリティを作った話
====================================================================================

.. post:: 2025-05-03
   :tags: Python, AWS, 非同期処理, lambda, litestar
   :author: sion908
   :language: ja
   :location: blog/2025

.. meta::
   :description: AWS Lambdaの非同期実行とローカルのasyncio処理を同じAPIで扱えるユーティリティを作成。LitestarでAPI化、CDKでデプロイまで自動化した構成を紹介。

はじめに
--------

AWS Lambdaの非同期実行とローカル開発の両立って意外と面倒ですよね。  
本記事では、asyncioによるローカル非同期処理と、Lambdaの非同期実行を同じAPIで扱えるユーティリティを作成し、LitestarでAPI化、CDKでデプロイまで自動化した構成を紹介します。

目的・背景
----------

- ローカルではasyncioで高速に非同期処理を試したい
- 本番はAWS Lambdaでスケールしたい
- API設計はモダンなPythonフレームワーク（Litestar）で
- デプロイ・管理はCDKで自動化したい

アーキテクチャ概要
------------------

.. code-block:: text

   +-------------+       +----------------+       +--------------------+
   | API Gateway |  -->  | API Lambda     |  -->  | Worker Lambda      |
   +-------------+       +----------------+       +--------------------+
            ↑                   |                        |
            |   (Litestar)      |   (async invoke)       | (async job)
            +-------------------+------------------------+

- API Gateway経由でリクエストを受け、API Lambda（Litestarアプリ）で処理
- 非同期ジョブはWorker Lambdaへinvoke
- ローカルではasyncioで同等の非同期実行

ソースコード
------------

`https://github.com/sion908/async_lambda_local <https://github.com/sion908/async_lambda_local>`_

ローカル＆Lambda両対応の非同期処理
----------------------------------

- ``async_lambda_invoker`` デコレータで、ローカル時はasyncio、Lambda時はboto3でinvoke
- 共通APIでどちらでも非同期ジョブをキックできる

.. code-block:: python

   from main import async_lambda_invoker

   @async_lambda_invoker
   async def process_job(data):
       # 非同期ジョブ本体

LitestarによるAPI実装
---------------------

- `/` でサービスのステータス確認
- `/process` で非同期ジョブをPOST
- VS Code REST Client用の `api_test.http` で簡単にAPIテスト

AWS CDKによるデプロイ自動化
--------------------------

- Lambda関数、IAMロール、API Gatewayなど全てCDKで定義
- ``manage.sh`` で ``./manage.sh deploy`` するだけで一発デプロイ
- ``.env`` でAWSプロファイルやリージョンを安全に管理

.. code-block:: bash

   ./manage.sh deploy

プロジェクト構成と管理
----------------------

- `main.py`: 非同期処理ロジックとAPI
- `infra/cdk/`: CDKスタック定義
- `src/lambda/`: Lambdaハンドラー
- `manage.sh`: 統合管理スクリプト
- `.env` & `.env.sample`: 設定ファイル
- `requirements.txt`, `requirements-dev.txt`: 依存関係管理

まとめ
------

- ローカルとLambdaの両方で同じAPIで非同期処理ができる
- LitestarでモダンなAPI開発
- CDKと管理スクリプトでデプロイも超簡単
- AWSプロファイルも安全に切り替え可能

---
