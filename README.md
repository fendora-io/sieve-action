# Sieve Security Scan · GitHub Action

**AI-powered security scanner for pull requests.** Sieve finds real vulnerabilities and suppresses false positives — so your team focuses on issues that actually matter.

> Built by [Fendora UG (haftungsbeschränkt)](https://fendora.io)

---

## Usage

```yaml
name: Security Scan

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  sieve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: fendora-io/sieve-action@v1
        with:
          api-key: ${{ secrets.SIEVE_API_KEY }}
          api-url: ${{ secrets.SIEVE_API_URL }}
```

## Setup

1. [Request access](mailto:contact@fendora.io) — we'll send you an API key and endpoint URL
2. Add `SIEVE_API_KEY` and `SIEVE_API_URL` to your repository secrets (**Settings → Secrets → Actions**)
3. Add the workflow above to `.github/workflows/sieve.yml`

That's it. Sieve will comment on every pull request with its findings.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `api-key` | ✅ | — | Your Sieve API key |
| `api-url` | ✅ | — | Sieve API endpoint (provided when you get your API key) |
| `repo-alias` | | repo name | Short name used in scan results |
| `fail-on-findings` | | `true` | Fail the check if real vulnerabilities are found |

## Outputs

| Output | Description |
|--------|-------------|
| `total` | Total findings scanned |
| `flagged` | Findings Sieve considers likely real |
| `scan-id` | Unique ID for this scan |

## Example PR comment

When Sieve finds issues it posts a comment on the PR:

```
## Sieve Security Scan ⚠️

2 finding(s) flagged as likely real — the rest were suppressed as false positives.

| Rule                  | File               | Line | Score |
|-----------------------|--------------------|------|-------|
| `sql-injection`       | `src/db/query.js`  | 42   | 0.94  |
| `subprocess-shell`    | `scripts/build.py` | 18   | 0.81  |

2 real · 14 suppressed · 16 total
```

When no issues are found:

```
## Sieve Security Scan ✅

No likely vulnerabilities found.

0 real · 9 suppressed · 9 total
```

## Don't fail the build

If you want Sieve to comment but not block merges:

```yaml
- uses: fendora-io/sieve-action@v1
  with:
    api-key: ${{ secrets.SIEVE_API_KEY }}
    api-url: ${{ secrets.SIEVE_API_URL }}
    fail-on-findings: "false"
```

## License

Apache 2.0 — see [LICENSE](LICENSE)

© 2026 Fendora UG (haftungsbeschränkt)
