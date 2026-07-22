# General Workspace Rules

このリポジトリで作業するすべてのエージェントは、以下の規則に従わなければなりません。

## 1. エージェント用ドキュメントの遵守
リポジトリルートにある [AGENTS.md](file:///Users/slep/Documents/myself/sion908_master/sion908/AGENTS.md) を読み、定義されている役割、制約、およびスキルを厳格に適用してください。

## 2. スキル使用のタイミング
以下のファイルやディレクトリを操作する際は、指定のスキルを必ず適用してください。

*   **ブログ記事のタグ変更、追加、または `tags.rst` の変更時:**
    *   スキル [.agents/skills/tag-management/SKILL.md](file:///Users/slep/Documents/myself/sion908_master/sion908/.agents/skills/tag-management/SKILL.md) をロードして実行してください。
*   **ブログ記事（`source/blog/**/*.rst`）の作成、編集時:**
    *   スキル [.agents/skills/ai-smell-detector/SKILL.md](file:///Users/slep/Documents/myself/sion908_master/sion908/.agents/skills/ai-smell-detector/SKILL.md) をロードし、文章の推敲に役立ててください。
