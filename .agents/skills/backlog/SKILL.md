---
name: backlog
description: Backlog API (v2) を使用して、課題（Issue）の取得・作成・更新、Wikiの参照、プロジェクト情報の取得などを支援するスキル。
---

# Backlog 連携スキル

Backlog API (v2) を利用して、プロジェクト管理ツール Backlog の課題（Issue）や Wiki、プロジェクト情報の取得・作成・更新を行うためのスキルです。

## 認証情報について
- **APIキー:** macOS Keychain（キーチェーンサービス名: `backlog-api-key`）または環境変数 `BACKLOG_API_KEY` から自動的に読み込まれます。
- **スペースドメイン:** macOS Keychain（キーチェーンサービス名: `backlog-domain`）または環境変数 `BACKLOG_DOMAIN`、あるいはコマンド引数 `--domain`（例: `yourspace.backlog.com` または `yourspace.backlog.jp`）から読み込まれます。
- **セキュリティルール:** APIキーをプロンプト、ログ、コミットメッセージ、生成ファイル等に出力・記載してはいけません。

## 初回設定（人間用）
macOS Keychain にスペースドメインやAPIキーを保存する場合：
```bash
# スペースドメインを登録（例: yourspace.backlog.com）
python3 .agents/skills/backlog/scripts/backlog.py --set-domain <DOMAIN>

# APIキーを登録
python3 .agents/skills/backlog/scripts/backlog.py --set-key <API_KEY>
```

---

## 主な使い方

スクリプトパス: `.agents/skills/backlog/scripts/backlog.py`

### 1. 認証ユーザーおよびスペース情報の確認
```bash
# 認証ユーザー情報の取得
python3 .agents/skills/backlog/scripts/backlog.py myself

# スペース情報の取得
python3 .agents/skills/backlog/scripts/backlog.py space
```

### 2. プロジェクト一覧の取得
```bash
python3 .agents/skills/backlog/scripts/backlog.py projects
```

### 3. 課題（Issue）の一覧・検索
```bash
# 自分に割り当てられているタスク（課題）を取得
python3 .agents/skills/backlog/scripts/backlog.py issues --mine

# プロジェクトキーまたはIDを指定して最新の課題を取得（デフォルト20件）
python3 .agents/skills/backlog/scripts/backlog.py issues --project <PROJECT_KEY_OR_ID>

# 自分の未対応・処理中タスクを取得
python3 .agents/skills/backlog/scripts/backlog.py issues --mine --status 1 --status 2

# キーワードで検索
python3 .agents/skills/backlog/scripts/backlog.py issues --keyword "バグ修正" --count 10
```

### 4. 課題詳細の取得
```bash
python3 .agents/skills/backlog/scripts/backlog.py issue <ISSUE_KEY_OR_ID>
# 例: python3 .agents/skills/backlog/scripts/backlog.py issue PROJ-123
```

### 5. 課題の追加
```bash
python3 .agents/skills/backlog/scripts/backlog.py add-issue \
  --project-id <PROJECT_ID> \
  --summary "課題の件名" \
  --issue-type-id <ISSUE_TYPE_ID> \
  --priority-id 3 \
  --description "課題の詳細説明文"
```

### 6. 課題へのコメント追加
```bash
python3 .agents/skills/backlog/scripts/backlog.py add-comment <ISSUE_KEY_OR_ID> --content "コメント内容"
```

### 7. Wiki の一覧・詳細取得
```bash
# Wikiページ一覧取得
python3 .agents/skills/backlog/scripts/backlog.py wikis --project-id <PROJECT_ID>

# Wikiページ内容取得
python3 .agents/skills/backlog/scripts/backlog.py wiki <WIKI_ID>
```
