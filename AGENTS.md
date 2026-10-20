# Workspace Agents Configuration

このリポジトリには、ドキュメント作成やブログ記事編集、タグ管理を支援するための特別なエージェント指示とスキルが設定されています。開発プロセスにおいて、エージェントは以下のガイドラインと定義されたスキルを適切なタイミングで使用しなければなりません。

---

## 1. エージェントの定義と役割

### 📝 AI Smell Detector (AI文章表現検知・修正)
AI生成にありがちな定型表現や不自然な文章構造を検出し、筆者独自の自然な文体を維持したまま修正を行います。
*   **適用タイミング:** ブログ記事（`source/blog/**/*.rst`）を執筆・編集する際、またはレビューする際。
*   **関連スキル:** [.agents/skills/ai-smell-detector/SKILL.md](file:///Users/slep/Documents/script/sion908_master/sion908/.agents/skills/ai-smell-detector/SKILL.md)

### 🏷️ Tag Manager Agent (タグ管理者)
ブログ記事のタグの一貫性を保ち、新規タグの検証と `tags.rst` の同期を行います。
*   **適用タイミング:** ブログ記事にタグを設定、変更する際、またはタグ一覧ページ（`source/tags.rst`）を更新する際。
*   **関連スキル:** [.agents/skills/tag-management/SKILL.md](file:///Users/slep/Documents/script/sion908_master/sion908/.agents/skills/tag-management/SKILL.md)
*   **制約事項・ルール:**
    1.  **事前確認の徹底:** 記事にタグを追加する前に、必ず [source/tags.rst](file:///Users/slep/Documents/script/sion908_master/sion908/source/tags.rst) を参照し、既存のタグ定義と一致しているか確認すること。
    2.  **大文字小文字・表記の統一:** `Lambda` と `lambda`、`litestar` と `Litestar` のような表記揺れを絶対に起こさないこと。`tags.rst` に定義されている表記を正とする。
    3.  **新規タグの検証:** `tags.rst` に存在しない新しいタグを定義する場合は、本当に新しいタグが必要か吟味した上で、[source/tags.rst](file:///Users/slep/Documents/script/sion908_master/sion908/source/tags.rst) の適切なカテゴリ（技術スタック/ドメイン/目的・タイプ）に追記し、リンクタグが正しく機能するように設定すること。
    4.  **自動チェックの実行:** タグの追加や修正を行った後は、スクリプトなどを用いて整合性が取れているかを必ず検証すること。

### 🔍 SEO Optimizer (SEO最適化)
ブログ記事の公開・修正前に、検索エンジンのインデックスやE-E-A-T、構造化データなどのSEO要件を満たしているか確認します。
*   **適用タイミング:** ブログ記事（`source/blog/**/*.rst`）を執筆・公開・編集する際、またはSEO改善を行う際。
*   **関連スキル:** [.agents/skills/seo-management/SKILL.md](file:///Users/slep/Documents/script/sion908_master/sion908/.agents/skills/seo-management/SKILL.md)

### 🎫 Connpass Event Manager (Connpassイベント連携)
connpass API (v2) を使用してイベント情報やグループの開催履歴を取得し、イベントレポートや告知の下書き作成を支援します。
*   **適用タイミング:** connpassのイベント情報やグループ開催履歴の取得、イベント参加/開催レポートの下書きを作成する際。
*   **関連スキル:** [.agents/skills/connpass/SKILL.md](file:///Users/slep/Documents/script/sion908_master/sion908/.agents/skills/connpass/SKILL.md)
*   **セキュリティルール:** APIトークンはプロンプト、ログ、コミットメッセージ、生成ファイル等に出力・記載しないこと。

---

## 2. スキルの実行ルール

エージェントは上記の適用タイミングにおいて、対応する `.agents/skills` 配下の `SKILL.md` に記載されたルールおよびプロセスを読み込み、それに従って操作を実行してください。
