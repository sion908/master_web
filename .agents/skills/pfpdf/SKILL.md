---
name: pfpdf
description: '@pfnet-research/pfpdf で信頼できる Markdown から日本語を含む PDF を作成・調整する。表紙、目次、テンプレート、ロゴ、フォントや組版の指定が必要なときに使う。既存 PDF の結合や編集には使わない。'
---

# pfpdf

Markdown を `@pfnet-research/pfpdf` で PDF にする。文書の内容、入力、出力、デザインは依頼と既存ファイルから決める。`memo/kaikou` は使い方の実例であり、他の文書の既定デザインではない。

## 入力と設定

- 入力は単一の `.md`、または直下の `*.md` をファイル名順に結合するディレクトリ。複数ファイルでは番号付きファイル名で順序を明示し、front matter は先頭ファイルに置く。
- 継続して使う文書設定は YAML front matter に記録する。タイトル、言語、著者、日付、シリーズ、テンプレート、表紙、目次、ロゴから必要なものを選ぶ。実際のキーと値は利用する pfpdf のバージョンで `--print-effective-config` と公式資料を確認する。
- 一回限りの変更は CLI 引数で上書きする。`--template`、`--title`、`--cover` / `--no-cover`、`--toc` / `--no-toc`、`--logo` / `--no-logo` を使える。CLI 指定は front matter より優先される。
- 同梱テンプレートは `academic`、`book`、`compact`、`default`、`notebook`、`pfn`、`technical`。用途と実際のプレビューで選ぶ。`memo/kaikou` の議事録は `pfn` を使っている。
- ロゴは利用権のあるファイルを指定する。front matter の相対パスは Markdown 所在地基準、CLI の相対パスは作業ディレクトリ基準。`--font-dir` はフォント候補を追加するだけなので、使用するフォントはカスタムテンプレートや CSS 側でも指定する。
- 同梱テンプレートで調整できない余白、色、書体、柱などは、公式の [カスタムテンプレート仕様](https://github.com/pfnet-research/pfpdf/blob/main/docs/tutorial.ja/06_templates-and-assets.md) に従い `template.html`、`style.css`、`vivliostyle.css` を持つディレクトリを作り `--template` で渡す。テンプレート形式にバージョン間の互換性保証はないため、再現性が必要なら pfpdf のバージョンを固定する。

例：

```md
---
title: 会議の記録
lang: ja
template: compact
cover: false
toc: false
---

# 会議の記録
```

## 実行と確認

1. Node.js が対象バージョンの要件を満たすか確認する。プロジェクトに導入済みならそのバージョンを使う。例: `memo/kaikou/node_modules/.bin/pfpdf --input memo/kaikou/2026_nagasaki_fg_furikaeri_gijiroku.md --output /tmp/gijiroku.pdf`。未導入なら、バージョンを固定した `npx --yes @pfnet-research/pfpdf@0.4.0` を使う例を提示し、文書の再現性が必要なら依存関係として固定する。
2. 必要なら同じ引数に `--print-effective-config` を付け、テンプレート・表紙・目次等が採用されたか確認する。タイトルは生成した PDF でも確認する。入力文書に未知のキーが混じる場合は `--strict-front-matter` で検査する。
3. PDF を生成し、ページ数、文字化け、表・画像の欠け、改ページ、表紙・目次、リンクを確認する。見た目が重要ならページを画像化して目視する。修正後は再生成して確認する。
4. 最終報告に入力、出力、主な設定、実行結果、未確認の点を記す。

信頼できる入力とテンプレートだけを変換する。pfpdf は raw HTML と script を実行し、ローカルファイルや外部 URL を参照できる。初回実行では Chromium のダウンロードが必要な場合がある。CLI や設定が変わった場合は [公式 README](https://github.com/pfnet-research/pfpdf/blob/main/README.ja.md) と `pfpdf --help` を確認する。
