# Architecture

Sieve by Fendora is a GitHub Action that runs on pull requests, scans code with Semgrep, filters findings through the Sieve API, and posts results as a PR comment.

## Actors

| Actor | Description |
|-------|-------------|
| **Developer** | Opens or updates a pull request in a consumer repository |
| **GitHub Actions** | Runs the action container on `pull_request` or `issue_comment` events |
| **Semgrep** | Static analysis engine run inside the action container |
| **Sieve API** | Fendora-hosted service that classifies findings (real vs. false positive) |
| **GitHub API** | Receives PR comments and reaction feedback via `GITHUB_TOKEN` |

## High-level flow

```
Developer opens PR
       │
       ▼
GitHub Actions triggers sieve-action container
       │
       ├──► Semgrep scan (OWASP ruleset, local repo checkout)
       │
       ├──► POST semgrep JSON + repo alias ──► Sieve API (/scan)
       │                                              │
       │◄──────────── classified findings ──────────────┘
       │
       ├──► Write job outputs (total, flagged, scan-id)
       │
       └──► POST PR comment via GitHub API (findings table + feedback links)
```

## Issue comment flow (`/sieve` slash command)

When a user comments `/sieve real <rule>` or `/sieve fp <rule>` on a PR:

1. The action reads the prior Sieve scan comment (embedded JSON payload).
2. Feedback is sent to the Sieve API (`/feedback`).
3. A confirmation comment is posted on the PR.

## Container layout

| File | Purpose |
|------|---------|
| `entrypoint.py` | Main orchestration: scan, API call, PR comment, slash commands |
| `Dockerfile` | Python 3.11 slim image; non-root `sieve` user |
| `requirements.txt` | Hash-locked Python dependencies (`semgrep`, `requests`) |
| `action.yml` | GitHub Action metadata (inputs, outputs, Docker image reference) |

## Release pipeline

Tag pushes (`v*`) trigger `.github/workflows/docker.yml`:

1. **Build** — Docker image pushed to `ghcr.io/fendora-io/sieve-action`
2. **Sign** — Cosign signs the image digest; sigstore bundle uploaded to the GitHub release

See [DEVELOPMENT.md](DEVELOPMENT.md) for build and dependency details.
