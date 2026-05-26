#!/usr/bin/env python3
"""
RSTファイル内のogp-cardディレクティブをスキャンし、OGP情報を取得して自動更新するスクリプト
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def fetch_ogp(url):
    """URLからOGP情報を取得"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        # OGP情報を取得
        og_title = None
        og_description = None
        og_image = None
        og_site_name = None

        # metaタグを検索
        for meta in soup.find_all('meta'):
            property_attr = meta.get('property') or meta.get('name')
            if property_attr == 'og:title':
                og_title = meta.get('content')
            elif property_attr == 'og:description':
                og_description = meta.get('content')
            elif property_attr == 'og:image':
                og_image = meta.get('content')
            elif property_attr == 'og:site_name':
                og_site_name = meta.get('content')
            elif property_attr == 'description':
                og_description = og_description or meta.get('content')

        # フォールバック
        title = og_title or (soup.title.string if soup.title else url)
        description = og_description or ''
        image = og_image or ''
        site_name = og_site_name or urlparse(url).netloc

        return {
            'title': title.strip() if title else url,
            'description': description.strip() if description else '',
            'image': image.strip() if image else '',
            'site_name': site_name.strip() if site_name else urlparse(url).netloc,
        }
    except Exception as e:
        print(f"OGP取得エラー: {url} - {e}", file=sys.stderr)
        return None


def update_rst_file(rst_path):
    """RSTファイルを更新"""
    rst_path = Path(rst_path)
    content = rst_path.read_text(encoding='utf-8')

    # ogp-cardディレクティブを検索
    pattern = r'\.\. ogp-card::\s+(\S+)'
    matches = list(re.finditer(pattern, content))

    if not matches:
        print(f"ogp-cardディレクティブが見つかりません: {rst_path}")
        return False

    updated = False
    for match in reversed(matches):  # 後ろから処理して位置ずれを防ぐ
        url = match.group(1)
        print(f"OGP情報を取得中: {url}")

        ogp_data = fetch_ogp(url)
        if not ogp_data:
            print(f"OGP情報の取得に失敗しました: {url}")
            continue

        # ディレクティブの終了位置を探す
        start_pos = match.start()
        end_pos = match.end()

        # 既にオプションがあるか確認
        lines_after = content[end_pos:].split('\n')
        option_lines = []
        line_count = 0

        for line in lines_after:
            if line.strip().startswith(':') and ':' in line:
                option_lines.append(line)
                line_count += 1
            elif line.strip() == '':
                line_count += 1
                if line_count > 2:  # 空行が2つ続いたら終了
                    break
            else:
                break

        # オプションを生成
        options = f"\n   :title: {ogp_data['title']}\n   :description: {ogp_data['description']}\n   :image: {ogp_data['image']}\n   :site_name: {ogp_data['site_name']}"

        # 既にオプションがある場合は置換、なければ追加
        if option_lines:
            # 既存のオプションを置換
            options_start = end_pos
            options_end = end_pos + sum(len(l) + 1 for l in option_lines)
            content = content[:options_start] + options + '\n' + content[options_end:]
        else:
            # 新規追加（URLの後ろに改行を入れてからオプション）
            content = content[:end_pos] + options + '\n' + content[end_pos:]

        updated = True
        print(f"OGP情報を追加しました: {url}")

    if updated:
        rst_path.write_text(content, encoding='utf-8')
        print(f"ファイルを更新しました: {rst_path}")
        return True
    else:
        print("更新は行われませんでした")
        return False


def main():
    if len(sys.argv) < 2:
        print("使用方法: python update_ogp_cards.py <rstファイルまたはディレクトリ>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        update_rst_file(target)
    elif target.is_dir():
        # ディレクトリ内のすべての.rstファイルを処理
        for rst_file in target.rglob('*.rst'):
            update_rst_file(rst_file)
    else:
        print(f"ファイルまたはディレクトリが見つかりません: {target}")
        sys.exit(1)


if __name__ == '__main__':
    main()
