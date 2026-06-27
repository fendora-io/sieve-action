#!/usr/bin/env python3
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid

import requests

SIEVE_URL     = "https://sieve.fendora.io/scan"
FEEDBACK_URL  = "https://sieve.fendora.io/feedback"
API_KEY       = "sieve-action-v1-dvE8NO1JN4YPclMhCE9TvRV75FJ3zYxz"
SCAN_MARKER   = "<!-- sieve-scan -->"
DATA_MARKER   = "sieve-findings"


def run_semgrep() -> dict:
    result = subprocess.run(
        ["semgrep", "--config", "p/owasp-top-ten", "--json", "--quiet", "."],
        capture_output=True, text=True,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"results": [], "errors": []}


def call_sieve(semgrep_output: dict, repo: str) -> dict:
    resp = requests.post(
        SIEVE_URL,
        json={"semgrep_output": semgrep_output, "repo": repo},
        headers={"Content-Type": "application/json", "X-API-Key": API_KEY},
        timeout=120,
    )
    if resp.status_code != 200:
        print(f"::error::Sieve API error {resp.status_code}: {resp.text[:500]}")
        sys.exit(1)
    return resp.json()


def _get_token() -> str:
    return (sys.argv[1] if len(sys.argv) > 1 else "") or os.environ.get("INPUT_GITHUB-TOKEN", "") or os.environ.get("GITHUB_TOKEN", "")


def _gh_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}


def post_pr_comment(result: dict, scan_id: str) -> None:
    token = _get_token()
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    if not token:
        print("::warning::GITHUB_TOKEN not available — skipping PR comment")
        return
    if not event_path:
        print("::warning::GITHUB_EVENT_PATH not set — skipping PR comment")
        return

    try:
        event = json.load(open(event_path))
        pr_number = event.get("pull_request", {}).get("number")
        repo = os.environ.get("GITHUB_REPOSITORY", "")
        if not pr_number:
            print("::warning::Not a pull_request event — skipping PR comment")
            return
        if not repo:
            print("::warning::GITHUB_REPOSITORY not set — skipping PR comment")
            return
    except Exception as e:
        print(f"::warning::Failed to read event file: {e}")
        return

    total      = result["total"]
    flagged    = result["flagged"]
    findings   = result["findings"]
    real       = sorted([f for f in findings if f["predicted_label"] == 1], key=lambda x: x["confidence_score"], reverse=True)
    suppressed = total - flagged

    if real:
        rows = "\n".join(
            f"| `{f['check_id'].split('.')[-1]}` | `{f['file']}` | {f['line_start']} | {f['confidence_score']:.2f} |"
            for f in real
        )
        hidden_data = json.dumps({
            "scan_id": scan_id,
            "findings": [
                {
                    "rule_id": f["check_id"],
                    "file_hash": hashlib.sha256(f["file"].encode()).hexdigest(),
                    "short": f["check_id"].split(".")[-1],
                }
                for f in real
            ]
        }, separators=(",", ":"))
        body = "\n".join([
            f"<!-- {DATA_MARKER}",
            hidden_data,
            "-->",
            "## Sieve Security Scan ⚠️",
            "",
            f"**{len(real)} finding(s) flagged as likely real** — the rest were suppressed as false positives.",
            "",
            "| Rule | File | Line | Score |",
            "|------|------|------|-------|",
            rows,
            "",
            f"_{flagged} real · {suppressed} suppressed · {total} total_",
            f"_scan\\_id: `{scan_id}`_",
            "",
            "💬 Reply `/sieve real` or `/sieve fp [rule]` to label findings.",
            "",
            "<sub>Powered by [Sieve](https://github.com/fendora-io/sieve-action) · AI security scanner by [Fendora](https://fendora.io)</sub>",
        ])
    else:
        body = (
            f"## Sieve Security Scan ✅\n\nNo likely vulnerabilities found.\n\n"
            f"_0 real · {suppressed} suppressed · {total} total_"
        )

    full_body = f"{SCAN_MARKER}\n{body}"
    api_base  = f"https://api.github.com/repos/{repo}"
    headers   = _gh_headers(token)

    comments = requests.get(f"{api_base}/issues/{pr_number}/comments", headers=headers).json()
    existing = next((c for c in comments if isinstance(c, dict) and SCAN_MARKER in c.get("body", "")), None)

    if existing:
        r = requests.patch(f"{api_base}/issues/comments/{existing['id']}", headers=headers, json={"body": full_body})
    else:
        r = requests.post(f"{api_base}/issues/{pr_number}/comments", headers=headers, json={"body": full_body})
    if r.status_code not in (200, 201):
        print(f"::warning::Failed to post PR comment: {r.status_code} {r.text[:200]}")


def handle_issue_comment() -> None:
    token = _get_token()
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    if not token or not event_path:
        return

    event = json.load(open(event_path))

    if not event.get("issue", {}).get("pull_request"):
        return

    body = event.get("comment", {}).get("body", "").strip()
    if not body.startswith("/sieve "):
        return

    parts = body.split()
    if len(parts) < 2 or parts[1] not in ("real", "fp"):
        return

    verdict     = parts[1]
    rule_filter = parts[2].lower() if len(parts) > 2 else None
    label       = 1 if verdict == "real" else 0

    pr_number = event["issue"]["number"]
    repo      = os.environ.get("GITHUB_REPOSITORY", "")
    api_base  = f"https://api.github.com/repos/{repo}"
    headers   = _gh_headers(token)

    comments = requests.get(f"{api_base}/issues/{pr_number}/comments", headers=headers).json()
    sieve_comment = next((c for c in comments if isinstance(c, dict) and SCAN_MARKER in c.get("body", "")), None)
    if not sieve_comment:
        return

    match = re.search(rf"<!-- {DATA_MARKER}\n(.*?)\n-->", sieve_comment["body"], re.DOTALL)
    if not match:
        return
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return

    scan_id  = data["scan_id"]
    findings = data["findings"]

    matched = [f for f in findings if not rule_filter or rule_filter in f["short"].lower()]
    if not matched:
        requests.post(f"{api_base}/issues/{pr_number}/comments", headers=headers,
                      json={"body": f"❓ No finding matching `{rule_filter}` in this scan."})
        return

    for f in matched:
        requests.get(FEEDBACK_URL, params={
            "scan_id":   scan_id,
            "rule_id":   f["rule_id"],
            "file_hash": f["file_hash"],
            "label":     label,
        }, timeout=10)

    emoji = "✅" if verdict == "real" else "🚫"
    word  = "real vulnerability" if verdict == "real" else "false positive"
    rules = ", ".join(f"`{f['short']}`" for f in matched)
    requests.post(f"{api_base}/issues/{pr_number}/comments", headers=headers,
                  json={"body": f"{emoji} Feedback recorded — {rules} marked as **{word}**."})


def write_outputs(result: dict, scan_id: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if not output_file:
        return
    with open(output_file, "a") as f:
        f.write(f"total={result['total']}\n")
        f.write(f"flagged={result['flagged']}\n")
        f.write(f"scan-id={scan_id}\n")


def main():
    if os.environ.get("GITHUB_EVENT_NAME") == "issue_comment":
        handle_issue_comment()
        return

    repo_alias       = os.environ.get("INPUT_REPO-ALIAS") or os.environ.get("GITHUB_REPOSITORY", "unknown")
    fail_on_findings = os.environ.get("INPUT_FAIL-ON-FINDINGS", "true").lower() == "true"

    print("Running security scan...")
    semgrep_output = run_semgrep()

    print("Analysing with Sieve...")
    result  = call_sieve(semgrep_output, repo_alias)
    scan_id = str(uuid.uuid4())

    total      = result["total"]
    flagged    = result["flagged"]
    findings   = result["findings"]
    suppressed = total - flagged

    print(f"Summary: {flagged} real · {suppressed} suppressed · {total} total")
    for f in sorted([x for x in findings if x["predicted_label"] == 1],
                    key=lambda x: x["confidence_score"], reverse=True):
        print(f"  [{f['confidence_score']:.2f}] {f['check_id']}  {f['file']}:{f['line_start']}")

    write_outputs(result, scan_id)
    post_pr_comment(result, scan_id)

    if fail_on_findings and flagged > 0:
        print(f"::error::Sieve flagged {flagged} likely real vulnerability(ies). Review the PR comment for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
