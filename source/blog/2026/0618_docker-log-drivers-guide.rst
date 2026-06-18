Dockerのログドライバー完全ガイド
==============================

.. post:: 2026-06-18
   :tags: Docker, ログ, 運用, チューニング
   :author: sion908
   :language: ja
   :location: blog/2026

.. meta::
   :description: 
     Dockerのログドライバーについて解説。
     json-file、local、journaldなど主要なログドライバーの特徴と設定方法を紹介。
     公式ドキュメントに基づいた引用付きガイド。


はじめに
--------

Dockerコンテナのログ管理は、運用において非常に重要な要素です。Dockerは複数のログドライバーを提供しており、用途に応じて適切なものを選択することで、効率的なログ管理が可能になります。本記事では、Dockerのログドライバーの種類と特徴、設定方法について解説します。

Dockerはデフォルトで、コンテナの標準出力（stdout）と標準エラー（stderr）を自動的にキャプチャし、ログとして保存します。これにより、アプリケーションがコンソールに出力する内容を後から確認できますが、意識せずに放置するとログファイルが肥大化し、ディスク容量を圧迫する原因になります。特に大量の出力を生成するコンテナや、長期間運用する環境では、適切なログ管理が不可欠です。

**TL;DR**
----

- Dockerはデフォルトで ``json-file`` ドライバーを使用し、stdout/stderrをJSON形式で保存
- ``json-file`` はデフォルトでログローテーションが無効なため、設定が必要
- ``local`` ドライバーはパフォーマンスとディスク使用に最適化され、デフォルトでローテーション有効
- ``local`` はバイナリ形式で人間が読めないが、運用環境では推奨されている
- ``daemon.json`` でデフォルトのログドライバーとオプションを設定可能


経緯
----

今、MediaMTX（メディアサーバー）をDocker環境で運用するべく、実装を行なっています。MediaMTXのGitHub Issue `#4772 <https://github.com/bluenviron/mediamtx/issues/4772>`_ では、ログローテーション機能の追加が検討されています。

このIssueでは、200台以上のRTSPカメラを使用している環境で、カメラがオフラインの際にMediaMTXが毎秒接続をリトライし、そのたびにエラーメッセージをログに出力するため、ログファイルがギガバイト単位になり、ディスクが埋まるリスクがあるという問題が報告されています。

::

  Problem In my setup, I use MediaMTX with over 200 RTSP cameras. Sometimes, cameras are offline or unreachable. When that happens, MediaMTX retries the RTSP connection roughly every second, and logs an error message each time.

  This leads to:
  - Gigabytes of log files
  - Risk of filling up the disk

（日本語訳: 私の環境では、200台以上のRTSPカメラでMediaMTXを使用しています。カメラがオフラインまたは到達不可能な場合、MediaMTXは毎秒RTSP接続をリトライし、そのたびにエラーメッセージをログに記録します。これにより、ギガバイト単位のログファイルが生成され、ディスクが埋まるリスクがあります。）

引用: `Log rotation or max log file size limit to prevent disk from filling up #4772 <https://github.com/bluenviron/mediamtx/issues/4772>`_

現在、この機能はMediaMTX本体には採用されていないため、Dockerのログドライバー設定で対応することにしました。


ログドライバーとは
------------------

Dockerのログドライバーは、実行中のコンテナやサービスから情報を取得するための仕組みです。Docker公式ドキュメントでは以下のように説明されています。

::

  Docker includes multiple logging mechanisms to help you get information from running containers and services. These mechanisms are called logging drivers. Each Docker daemon has a default logging driver, which each container uses unless you configure it to use a different logging driver, or log driver for short.

（日本語訳: Dockerには、実行中のコンテナやサービスから情報を取得するための複数のログメカニズムが含まれています。これらのメカニズムはログドライバーと呼ばれます。各Dockerデーモンにはデフォルトのログドライバーがあり、異なるログドライバーを使用するように設定しない限り、各コンテナがそれを使用します。）

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_

各Dockerデーモンにはデフォルトのログドライバーがあり、コンテナごとに異なるログドライバーを設定することも可能です。


デフォルトのログドライバー
--------------------------

Dockerのデフォルトのログドライバーは ``json-file`` です。

::

  As a default, Docker uses the `json-file` logging driver, which caches container logs as JSON internally.

（日本語訳: デフォルトでは、Dockerは `json-file` ログドライバーを使用し、コンテナログをJSONとして内部的にキャッシュします。）

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_

ただし、 ``json-file`` はデフォルトでログローテーションを行わないため、大量の出力を生成するコンテナではディスク容量を圧迫する可能性があります。そのため、公式ドキュメントでは ``local`` ログドライバーの使用が推奨されています。

::

  Use the local logging driver to prevent disk-exhaustion. By default, no log-rotation is performed. As a result, log-files stored by the default json-file logging driver logging driver can cause a significant amount of disk space to be used for containers that generate much output, which can lead to disk space exhaustion.

（日本語訳: ディスク枯渇を防ぐためにlocalログドライバーを使用してください。デフォルトではログローテーションは行われません。その結果、デフォルトのjson-fileログドライバーに保存されたログファイルは、大量の出力を生成するコンテナでディスク容量を大幅に使用する可能性があり、ディスク容量の枯渇につながる可能性があります。）

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_

::

  For other situations, the local logging driver is recommended as it performs log-rotation by default, and uses a more efficient file format.

（日本語訳: その他の状況では、デフォルトでログローテーションを行い、より効率的なファイル形式を使用するため、localログドライバーが推奨されます。）

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_


サポートされているログドライバー
------------------------------

Dockerでサポートされている主なログドライバーは以下の通りです。

- ``none``: コンテナのログが利用できず、 ``docker logs`` も出力を返しません
- ``local``: パフォーマンスとディスク使用に最適化されたカスタム形式でログを保存
- ``json-file``: ログをJSON形式でフォーマット。Dockerのデフォルト
- ``syslog``: syslogサーバーにログをルーティング
- ``journald``: systemd journalにログを送信
- ``gelf``: GraylogやLogstashなどのGELFエンドポイントにログを送信
- ``fluentd``: fluentdデーモン（forward input）にログメッセージを送信
- ``awslogs``: Amazon CloudWatch Logsにログを送信
- ``splunk``: HTTP Event Collectorを使用してSplunkにログメッセージを送信
- ``etwlogs``: Event Tracing for Windows (ETW)イベントとしてログメッセージを書き込み（Windowsのみ）
- ``gcplogs``: Google Cloud Platform (GCP) Loggingにログメッセージを書き込み

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_


主要なログドライバーの詳細
--------------------------

json-file
~~~~~~~~~

``json-file`` はDockerのデフォルトのログドライバーです。コンテナの標準出力と標準エラーをJSON形式でファイルに書き込みます。

::

  By default, Docker captures the standard output (and standard error) of all your containers, and writes them in files using the JSON format. The JSON format annotates each line with its origin (stdout or stderr) and its timestamp.

（日本語訳: デフォルトでは、Dockerはすべてのコンテナの標準出力（および標準エラー）をキャプチャし、JSON形式を使用してファイルに書き込みます。JSON形式は、各行に出典（stdoutまたはstderr）とタイムスタンプを注釈として付けます。）

引用: `JSON File logging driver | Docker Docs <https://docs.docker.com/engine/logging/drivers/json-file/>`_

ログの形式は以下のようになります：

.. code-block:: json

  {
    "log": "Log line is here\n",
    "stream": "stdout",
    "time": "2019-01-01T11:11:11.111111111Z"
  }

**主なオプション:**

- ``max-size``: ログローテーション前の最大サイズ（例: ``10m``）
- ``max-file``: 保持するログファイルの最大数（例: ``3``）
- ``compress``: ローテーションされたログの圧縮（デフォルト: ``false``）

**設定例:**

.. code-block:: json

  {
    "log-driver": "json-file",
    "log-opts": {
      "max-size": "10m",
      "max-file": "3"
    }
  }


local
~~~~~

``local`` ログドライバーは、パフォーマンスとディスク使用に最適化された内部ストレージにログを書き込みます。

::

  The local logging driver captures output from container's stdout/stderr and writes them to an internal storage that's optimized for performance and disk use.

（日本語訳: localログドライバーは、コンテナのstdout/stderrからの出力をキャプチャし、パフォーマンスとディスク使用に最適化された内部ストレージに書き込みます。）

引用: `Local file logging driver | Docker Docs <https://docs.docker.com/engine/logging/drivers/local/>`_

**特徴:**

- パフォーマンスとディスク使用に最適化されたバイナリ形式
- デフォルトでログローテーションが有効（コンテナあたり100MB保持）
- 自動圧縮でディスクサイズを削減
- 外部ツールでの直接アクセスは推奨されない（Dockerデーモン専用）

::

  The local logging driver uses file-based storage. These files are designed to be exclusively accessed by the Docker daemon. Interacting with these files with external tools may interfere with Docker's logging system and result in unexpected behavior, and should be avoided.

（日本語訳: localログドライバーはファイルベースのストレージを使用します。これらのファイルはDockerデーモン専用に設計されています。外部ツールでこれらのファイルを操作すると、Dockerのログシステムに干渉し、予期しない動作を引き起こす可能性があるため、避けるべきです。）

**json-fileとの比較:**

- **json-file**: テキスト形式（JSON）、人間が読める、外部ツールで解析可能、デフォルトでローテーション無効
- **local**: バイナリ形式、人間が読めない、Dockerデーモン経由でのみアクセス可能、デフォルトでローテーション有効

**どちらを選ぶべきか:**

- **json-fileを選ぶ場合**: ログを直接確認・解析したい、外部ツール（grep、jqなど）で処理したい、開発環境
- **localを選ぶ場合**: パフォーマンスを重視したい、ディスク使用を最小化したい、運用環境でログローテーションを確実に行いたい

**今回の環境での採用判断:**

今回のMediaMTX環境では、localドライバーではなくjson-fileドライバーを採用しました。理由は以下の通りです：

- バイナリ形式でログが保存されるため、メンテナンス性が低く、トラブルシューティングが困難
- 外部ツールでの直接アクセスが推奨されず、ログ確認や解析が不便
- 標準的なjson-fileで十分にログローテーションを設定でき、実績も豊富

これらの理由から、今回はjson-fileドライバーを使用し、適切なローテーション設定を行うことで対応することにしました。

デフォルトで以下の設定が適用されています：

- コンテナあたり100MBのログメッセージを保持
- 自動圧縮でディスクサイズを削減
- デフォルトのファイルサイズ: 20MB
- デフォルトのファイル数: 5

**主なオプション:**

- ``max-size``: ログローテーション前の最大サイズ（デフォルト: ``20m``）
- ``max-file``: 保持するログファイルの最大数（デフォルト: ``5``）
- ``compress``: ローテーションされたログの圧縮（デフォルト: ``true``）

**設定例:**

.. code-block:: json

  {
    "log-driver": "local",
    "log-opts": {
      "max-size": "10m",
      "max-file": "3"
    }
  }


journald
~~~~~~~~

``journald`` ログドライバーは、コンテナログをsystemd journalに送信します。

::

  The journald logging driver sends container logs to the systemd journal. Log entries can be retrieved using the journalctl command, through use of the journal API, or using the docker logs command.

（日本語訳: journaldログドライバーは、コンテナログをsystemd journalに送信します。ログエントリは、journalctlコマンド、journal APIの使用、またはdocker logsコマンドを使用して取得できます。）

引用: `Journald logging driver | Docker Docs <https://docs.docker.com/engine/logging/drivers/journald/>`_

**主なオプション:**

- ``tag``: journaldログの ``CONTAINER_TAG`` と ``SYSLOG_IDENTIFIER`` 値を設定するテンプレート
- ``labels``: メッセージに含めるラベルのキーのカンマ区切りリスト
- ``env``: メッセージに含める環境変数のキーのカンマ区切りリスト

**設定例:**

.. code-block:: bash

  docker run \
    --log-driver=journald \
    --log-opt labels=location \
    --log-opt env=TEST \
    --env "TEST=false" \
    your/application

**ログの取得:**

.. code-block:: bash

  # journalctlでログを取得
  journalctl CONTAINER_NAME=web

  # JSON形式で取得
  journalctl -o json CONTAINER_NAME=web


ログドライバーの設定方法
------------------------

デフォルトログドライバーの設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dockerデーモンのデフォルトログドライバーを設定するには、 ``daemon.json`` ファイルを編集します。

::

  To configure the Docker daemon to default to a specific logging driver, set the value of log-driver to the name of the logging driver in the daemon.json configuration file.

（日本語訳: Dockerデーモンを特定のログドライバーをデフォルトにするように設定するには、daemon.json設定ファイルでlog-driverの値をログドライバーの名前に設定します。）

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_

**daemon.jsonの例:**

.. code-block:: json

  {
    "log-driver": "local",
    "log-opts": {
      "max-size": "10m"
    }
  }

設定後、Dockerを再起動する必要があります。既存のコンテナは新しい設定を自動的には使用しません。


コンテナごとの設定
~~~~~~~~~~~~~~~~~~

コンテナ起動時に ``--log-driver`` フラグを使用して、デーモンのデフォルトとは異なるログドライバーを設定できます。

::

  When you start a container, you can configure it to use a different logging driver than the Docker daemon's default, using the --log-driver flag.

（日本語訳: コンテナを起動するとき、--log-driverフラグを使用して、Dockerデーモンのデフォルトとは異なるログドライバーを使用するようにコンテナを設定できます。）

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_

**例:**

.. code-block:: bash

  # noneドライバーを使用
  docker run -it --log-driver none alpine ash

  # localドライバーを使用
  docker run --log-driver local --log-opt max-size=10m alpine echo hello world


現在の設定の確認
~~~~~~~~~~~~~~~~

現在のデフォルトログドライバーを確認するには：

.. code-block:: bash

  docker info --format '{{.LoggingDriver}}'

コンテナのログドライバーを確認するには：

.. code-block:: bash

  docker inspect -f '{{.HostConfig.LogConfig.Type}}' <CONTAINER>


ログドライバーの制限事項
------------------------

ログドライバーを使用する際の制限事項は以下の通りです。

::

  - Reading log information requires decompressing rotated log files, which causes a temporary increase in disk usage (until the log entries from the rotated files are read) and an increased CPU usage while decompressing.
  - The capacity of the host storage where the Docker data directory resides determines the maximum size of the log file information.

（日本語訳: ログ情報を読み取るにはローテーションされたログファイルを解凍する必要があり、これによりディスク使用量が一時的に増加し（ローテーションされたファイルからのログエントリが読み取られるまで）、解凍中にCPU使用量が増加します。Dockerデータディレクトリがあるホストストレージの容量が、ログファイル情報の最大サイズを決定します。）

引用: `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_

つまり：

- ローテーションされたログファイルを読み取るには解凍が必要で、一時的にディスク使用量とCPU使用量が増加する
- ログファイルの最大サイズは、Dockerデータディレクトリがあるホストストレージの容量によって決まる


まとめ
------

Dockerのログドライバーは、用途に応じて適切に選択することが重要です。

- **開発環境**: ``json-file`` （デフォルト）で十分
- **本番環境**: ``local`` （ローテーションあり）が推奨
- **集中ログ管理**: ``syslog`` 、 ``fluentd`` 、 ``awslogs`` など
- **systemd環境**: ``journald``

特にディスク容量の問題を避けるため、本番環境では ``local`` ログドライバーの使用、または ``json-file`` で適切なローテーション設定を行うことを推奨します。


参考文献
--------

- `Configure logging drivers | Docker Docs <https://docs.docker.com/engine/logging/configure/>`_
- `JSON File logging driver | Docker Docs <https://docs.docker.com/engine/logging/drivers/json-file/>`_
- `Local file logging driver | Docker Docs <https://docs.docker.com/engine/logging/drivers/local/>`_
- `Journald logging driver | Docker Docs <https://docs.docker.com/engine/logging/drivers/journald/>`_
