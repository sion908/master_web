#!/bin/bash

# Sphinx Slides ローカルサーバー起動スクリプト
# 使い方: ./serve.sh [-p PORT] [-b] [-s]

# デフォルト設定
DEFAULT_PORT=8080
PORT=$DEFAULT_PORT
BUILD_ONLY=false
SKIP_BUILD=false

# 引数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -p)
            PORT="$2"
            shift 2
            ;;
        -b)
            BUILD_ONLY=true
            shift
            ;;
        -s)
            SKIP_BUILD=true
            shift
            ;;
        -h|--help)
            echo "使い方: $0 [-p PORT] [-b] [-s]"
            echo ""
            echo "オプション:"
            echo "  -p PORT        サーバーのポートを指定 (デフォルト: $DEFAULT_PORT)"
            echo "  -b             ビルドのみ実行し、サーバーは起動しない"
            echo "  -s             ビルドをスキップし、サーバーのみ起動"
            echo "  -h, --help     このヘルプを表示"
            echo ""
            echo "例:"
            echo "  $0                    # ビルド&サーバー起動（デフォルト）"
            echo "  $0 -p 3000           # ポート3000でビルド&サーバー起動"
            echo "  $0 -b                 # ビルドのみ実行"
            echo "  $0 -s                 # ビルドをスキップしてサーバー起動"
            exit 0
            ;;
        *)
            echo "不明なオプション: $1"
            echo "使い方: $0 [-p PORT] [-b] [-s]"
            exit 1
            ;;
    esac
done

# スクリプトディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境の有無を確認 (.venv)
if ! command -v uv &> /dev/null; then
    echo "❌ uvコマンドが見つかりません"
    echo "まず uv をインストールしてください (例: brew install uv)"
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "📦 uv環境をセットアップします..."
    uv sync
    uv run playwright install
fi

# ビルド実行（スキップオプションがなければ）
if [ "$SKIP_BUILD" = false ]; then
    echo "🔨 スライドをビルド中..."
    if uv run make all-slides; then
        echo "✅ ビルド完了"
    else
        echo "❌ ビルドに失敗しました"
        exit 1
    fi
else
    echo "⏭️  ビルドをスキップします"
fi

# ビルドのみモードの場合はここで終了
if [ "$BUILD_ONLY" = true ]; then
    echo "📦 ビルド完了。ファイルは build/revealjs/ にあります"
    exit 0
fi

# ポートが使用中かチェック
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  ポート $PORT は既に使用中です"
    echo "別のポートを試してください: $0 -p 8081"
    exit 1
fi

# ビルドファイルの存在確認
if [ ! -d "build/revealjs" ]; then
    echo "❌ ビルドファイルが見つかりません"
    echo "まずビルドを実行してください: $0"
    exit 1
fi

# URLをクリップボードにコピー
URL="http://localhost:$PORT"
if command -v pbcopy >/dev/null 2>&1; then
    echo "$URL" | pbcopy
    echo "📋 URLをクリップボードにコピーしました: $URL"
else
    echo "ℹ️  pbcopyが利用できません。URL: $URL"
fi

# サーバー起動
echo "🚀 サーバーを起動します: $URL"
echo "停止するには Ctrl+C を押してください"
echo ""

uv run python -m http.server $PORT --directory build/revealjs
