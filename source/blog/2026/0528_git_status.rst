Gitの状態を正しく理解する
===========================

.. post:: 2026-05-28
   :tags: Git, チュートリアル, AIエージェント
   :author: sion908
   :language: ja
   :location: blog/2026

.. meta::
   :description: 
     Gitの状態（working tree / staged / committed）を正しく理解することで、
     AIエージェントへの指示がより正確になります。


Gitを使っていると「addしていない」「commitしていない」といった状態で混乱することがよくあります。
Gitの状態を正しく理解することで、より効率的にバージョン管理ができるようになります。
特にAIエージェントにGit操作を依頼する際、状態を正しく伝えることが重要です。


Gitの3つの状態
--------------

Gitには主に3つの領域があります。

.. list-table:: Gitの3つの状態
   :width: 100%
   :header-rows: 1

   * - 状態
     - Git上の呼び方
     - 意味
   * - commitされたもの
     - committed / HEAD
     - リポジトリに記録済み
   * - 修正されたもの
     - modified / working tree
     - ファイルは変えたが、まだaddしていない
   * - addされたもの
     - staged / index
     - 次のcommitに入る予定


ワークフロー
----------

Gitの基本的な流れは以下の通りです。

.. code-block:: text

   編集する
     ↓
   modified（working tree）
     ↓ git add
   staged（index / staging area）
     ↓ git commit
   committed（repository）

**各状態の遷移**

.. list-table:: 
   :width: 100%
   :header-rows: 1

   * - 操作
     - 前の状態
     - 後の状態
     - コマンド
   * - ファイルを編集
     - committed
     - modified
     - エディタで編集
   * - 変更を追加
     - modified
     - staged
     - ``git add``
   * - 変更を確定
     - staged
     - committed
     - ``git commit``


実務上の覚え方
--------------

「commitされたもの」は状態というより、すでに履歴に保存されたスナップショットです。
実務上は以下のように覚えるのが一番正確です。

- **working tree**: まだaddしていない変更
- **index/staging area**: add済みの変更
- **repository**: commit済みの履歴


各状態の確認方法
----------------

.. code-block:: bash

   # working treeの状態を確認
   git status

   # stagedの変更を確認
   git diff --staged

   # commit済みの履歴を確認
   git log


AIエージェントへの伝え方
----------------------

AIエージェントにGitの操作を依頼する際、状態を正しく伝えることで意図した操作ができます。

**良い例**

- 「working treeにある変更を全てaddして」
- 「stagedにある変更をcommitして」
- 「直近のcommitを amended して」

**悪い例**

- 「変更を保存して」→（addかcommitか曖昧）
- 「コミットして」→（何をcommitするか不明）

**状態確認の依頼**

- 「現在のworking treeの状態を教えて」→ ``git status``
- 「stagedされている変更の差分を見せて」→ ``git diff --staged``


まとめ
----

Gitの状態を理解することで、意図しないcommitを防いだり、変更を正しく管理できるようになります。
特に「まだaddしていない変更」と「add済みの変更」の違いを意識することが重要です。

AIエージェントにGit操作を依頼する際も、状態（working tree / staged / committed）を明確に伝えることで、より正確な操作が可能になります。
