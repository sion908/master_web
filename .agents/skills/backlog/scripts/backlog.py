#!/usr/bin/env python3
"""
Backlog API (v2) 操作用 CLI スクリプト。
macOS Keychain または環境変数から API キーおよびスペースドメインを取得して Backlog と連携します。
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

KEYCHAIN_SERVICE_KEY = "backlog-api-key"
KEYCHAIN_SERVICE_DOMAIN = "backlog-domain"


def get_from_keychain(service: str) -> Optional[str]:
    """macOS Keychain から値を取得"""
    if platform.system() != "Darwin":
        return None
    user = os.environ.get("USER", "")
    if not user:
        return None
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-a", user, "-s", service, "-w"],
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return None


def save_to_keychain(service: str, val: str) -> bool:
    """macOS Keychain に値を保存"""
    if platform.system() != "Darwin":
        print("Keychain storage is only available on macOS.", file=sys.stderr)
        return False
    user = os.environ.get("USER", "")
    if not user:
        print("Cannot determine current user.", file=sys.stderr)
        return False
    try:
        res = subprocess.run(
            ["security", "add-generic-password", "-U", "-a", user, "-s", service, "-w", val],
            check=False,
        )
        return res.returncode == 0
    except Exception as e:
        print(f"Failed to store in Keychain: {e}", file=sys.stderr)
        return False


def get_credentials(cli_domain: Optional[str] = None, cli_key: Optional[str] = None) -> tuple[str, str]:
    """APIキーとドメインを取得（優先順位: 引数 > 環境変数 > キーチェーン）"""
    api_key = cli_key or os.environ.get("BACKLOG_API_KEY") or get_from_keychain(KEYCHAIN_SERVICE_KEY)
    domain = cli_domain or os.environ.get("BACKLOG_DOMAIN") or get_from_keychain(KEYCHAIN_SERVICE_DOMAIN)

    if not api_key:
        print(
            "Error: Backlog API Key is not set.\n"
            "Set BACKLOG_API_KEY environment variable or save to Keychain using:\n"
            "  python3 scripts/backlog.py --set-key <API_KEY>",
            file=sys.stderr,
        )
        sys.exit(1)

    if not domain:
        print(
            "Error: Backlog domain is not set.\n"
            "Set BACKLOG_DOMAIN environment variable (e.g. yourspace.backlog.com or yourspace.backlog.jp) or save to Keychain using:\n"
            "  python3 scripts/backlog.py --set-domain <DOMAIN>",
            file=sys.stderr,
        )
        sys.exit(1)

    # ドメイン形式の正規化（https:// や 末尾のスラッシュを除去）
    domain = domain.strip().replace("https://", "").replace("http://", "").rstrip("/")
    return domain, api_key


def api_request(
    domain: str,
    api_key: str,
    endpoint: str,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Any:
    """Backlog API リクエストを実行"""
    base_url = f"https://{domain}/api/v2{endpoint}"

    query_params = dict(params or {})
    query_params["apiKey"] = api_key
    url = f"{base_url}?{urllib.parse.urlencode(query_params, doseq=True)}"

    req_data = None
    headers = {"User-Agent": "Antigravity-Backlog-Skill/1.0"}

    if data is not None:
        req_data = urllib.parse.urlencode(data, doseq=True).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as res:
            res_body = res.read().decode("utf-8")
            if not res_body:
                return {}
            return json.loads(res_body)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(error_body)
            messages = [err.get("message", "") for err in err_json.get("errors", [])]
            err_detail = " / ".join(messages) or error_body
        except Exception:
            err_detail = error_body
        print(f"API Error ({e.code}): {err_detail}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Backlog API v2 CLI")
    parser.add_argument("--domain", help="Backlog space domain (e.g. example.backlog.com)")
    parser.add_argument("--key", help="Backlog API key (optional, prefers Keychain/Env)")
    parser.add_argument("--set-key", help="Save API key to macOS Keychain and exit")
    parser.add_argument("--set-domain", help="Save Backlog space domain to macOS Keychain and exit")

    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # myspace: スペース情報取得
    subparsers.add_parser("space", help="Get space details")

    # myself: 認証ユーザー情報
    subparsers.add_parser("myself", help="Get current user info")

    # projects: プロジェクト一覧
    subparsers.add_parser("projects", help="List projects")

    # issues: 課題一覧取得
    parser_issues = subparsers.add_parser("issues", help="List/Search issues")
    parser_issues.add_argument("--project", "-p", action="append", help="Project ID or Key (repeatable)")
    parser_issues.add_argument("--count", "-n", type=int, default=20, help="Number of issues to fetch (default: 20)")
    parser_issues.add_argument("--status", action="append", type=int, help="Status ID (repeatable)")
    parser_issues.add_argument("--keyword", "-k", help="Keyword search")
    parser_issues.add_argument("--mine", action="store_true", help="Filter issues assigned to myself")
    parser_issues.add_argument("--assignee", action="append", type=int, help="Assignee User ID (repeatable)")

    # issue: 課題詳細取得
    parser_issue = subparsers.add_parser("issue", help="Get issue details")
    parser_issue.add_argument("issue_id_or_key", help="Issue ID or Key (e.g. PROJ-123)")

    # add-issue: 課題追加
    parser_add_issue = subparsers.add_parser("add-issue", help="Add new issue")
    parser_add_issue.add_argument("--project-id", required=True, type=int, help="Project ID")
    parser_add_issue.add_argument("--summary", required=True, help="Issue summary")
    parser_add_issue.add_argument("--issue-type-id", required=True, type=int, help="Issue Type ID")
    parser_add_issue.add_argument("--priority-id", required=True, type=int, help="Priority ID (2=High, 3=Normal, 4=Low)")
    parser_add_issue.add_argument("--description", help="Issue description")
    parser_add_issue.add_argument("--assignee-id", type=int, help="Assignee User ID")
    parser_add_issue.add_argument("--parent-issue-id", type=int, help="Parent Issue ID")
    parser_add_issue.add_argument("--category-id", action="append", type=int, help="Category ID (repeatable)")

    # update-issue: 課題更新
    parser_update_issue = subparsers.add_parser("update-issue", help="Update issue")
    parser_update_issue.add_argument("issue_id_or_key", help="Issue ID or Key (e.g. PROJ-123)")
    parser_update_issue.add_argument("--summary", help="Issue summary")
    parser_update_issue.add_argument("--description", help="Issue description")
    parser_update_issue.add_argument("--status-id", type=int, help="Status ID")
    parser_update_issue.add_argument("--comment", help="Comment for this update")

    # add-comment: 課題にコメント追加
    parser_comment = subparsers.add_parser("add-comment", help="Add comment to issue")
    parser_comment.add_argument("issue_id_or_key", help="Issue ID or Key (e.g. PROJ-123)")
    parser_comment.add_argument("--content", required=True, help="Comment content")

    # wikis: Wiki一覧
    parser_wikis = subparsers.add_parser("wikis", help="List wiki pages")
    parser_wikis.add_argument("--project-id", required=True, type=int, help="Project ID")

    # wiki: Wiki詳細
    parser_wiki = subparsers.add_parser("wiki", help="Get wiki page content")
    parser_wiki.add_argument("wiki_id", type=int, help="Wiki Page ID")

    args = parser.parse_args()

    if args.set_key:
        if save_to_keychain(KEYCHAIN_SERVICE_KEY, args.set_key):
            print("API key successfully saved to macOS Keychain.")
        sys.exit(0)

    if args.set_domain:
        cleaned_domain = args.set_domain.strip().replace("https://", "").replace("http://", "").rstrip("/")
        if save_to_keychain(KEYCHAIN_SERVICE_DOMAIN, cleaned_domain):
            print(f"Domain '{cleaned_domain}' successfully saved to macOS Keychain.")
        sys.exit(0)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    domain, api_key = get_credentials(cli_domain=args.domain, cli_key=args.key)

    if args.command == "space":
        res = api_request(domain, api_key, "/space")
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "myself":
        res = api_request(domain, api_key, "/users/myself")
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "projects":
        res = api_request(domain, api_key, "/projects")
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "issues":
        params: Dict[str, Any] = {"count": args.count}
        if args.project:
            params["projectId[]"] = args.project
        if args.status:
            params["statusId[]"] = args.status
        if args.keyword:
            params["keyword"] = args.keyword
        if args.mine:
            # 認証ユーザー自身のIDを取得して設定
            myself = api_request(domain, api_key, "/users/myself")
            my_id = myself.get("id")
            if my_id:
                params["assigneeId[]"] = [my_id]
        elif args.assignee:
            params["assigneeId[]"] = args.assignee
        res = api_request(domain, api_key, "/issues", params=params)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "issue":
        res = api_request(domain, api_key, f"/issues/{args.issue_id_or_key}")
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "add-issue":
        data = {
            "projectId": args.project_id,
            "summary": args.summary,
            "issueTypeId": args.issue_type_id,
            "priorityId": args.priority_id,
        }
        if args.description:
            data["description"] = args.description
        if args.assignee_id:
            data["assigneeId"] = args.assignee_id
        if args.parent_issue_id:
            data["parentIssueId"] = args.parent_issue_id
        if args.category_id:
            data["categoryId[]"] = args.category_id
        res = api_request(domain, api_key, "/issues", method="POST", data=data)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "update-issue":
        data = {}
        if args.summary:
            data["summary"] = args.summary
        if args.description:
            data["description"] = args.description
        if args.status_id:
            data["statusId"] = args.status_id
        if args.comment:
            data["comment"] = args.comment
        res = api_request(domain, api_key, f"/issues/{args.issue_id_or_key}", method="PATCH", data=data)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "add-comment":
        data = {"content": args.content}
        res = api_request(domain, api_key, f"/issues/{args.issue_id_or_key}/comments", method="POST", data=data)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "wikis":
        params = {"projectIdOrKey": args.project_id}
        res = api_request(domain, api_key, "/wikis", params=params)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    elif args.command == "wiki":
        res = api_request(domain, api_key, f"/wikis/{args.wiki_id}")
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
