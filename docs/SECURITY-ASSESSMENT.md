# Security Assessment

This document summarizes the most likely and impactful security risks for **Sieve by Fendora** (the `fendora-io/sieve-action` GitHub Action), assessed at release **v1.4.3**.

## Scope

- Action container (`entrypoint.py`, `Dockerfile`, dependencies)
- CI/CD pipelines (`.github/workflows/`)
- Data flows to external services (Sieve API, GitHub API)

Out of scope: the Sieve API backend (report issues to **security@fendora.io**).

## Threat summary

| Risk | Likelihood | Impact | Mitigations |
|------|------------|--------|-------------|
| **Malicious PR code execution** | High (by design) | Medium | Action runs Semgrep on untrusted checkout inside an isolated container; non-root user; PR workflows use `contents: read` only |
| **GITHUB_TOKEN abuse** | Low | High | Token scoped to consumer workflow permissions; action only posts PR comments |
| **Dependency supply chain** | Medium | High | Hash-locked `requirements.txt`, pinned base image digest, Dependabot, CodeQL, Semgrep in CI |
| **Secrets in repository** | Low | High | No real secrets in repo; API key is a public client identifier; org secrets only in trusted release workflow |
| **CI/CD injection via metadata** | Medium | High | Workflow metadata validated before shell use (`docker.yml`); least-privilege `permissions` on all workflows |
| **Data exfiltration to Sieve API** | Medium | Medium | Only Semgrep findings (rule, path, snippet) sent — documented in README Data & Privacy section |
| **Tampered release artifacts** | Low | High | Semver tags, Cosign signing, sigstore bundles on GitHub releases |

## Trust boundaries

1. **Consumer repo PR code** — untrusted; scanned read-only by Semgrep inside the container.
2. **Action container image** — trusted when pulled from `ghcr.io/fendora-io/sieve-action` at a pinned tag with Cosign verification.
3. **Sieve API** — trusted third-party service; TLS in transit; public client API key (not a secret).
4. **GitHub API** — trusted; authenticated with the workflow's `GITHUB_TOKEN`.

## Residual risks

- Semgrep or Python dependency vulnerabilities between release cycles (mitigated by Dependabot and security scanning in CI).
- Compromise of maintainer accounts with admin access (mitigated by MFA, branch protection, required reviews).
- False negatives in AI classification (operational risk, not a direct exploit path).

## Review cadence

This assessment is reviewed when:

- A new major/minor release is cut
- Architecture or data flows change materially
- A security advisory is published

Last reviewed: **2026-07-13**

## Attack surface analysis (SA-03.02)

### Critical code paths

| Path | Input | Risk | Controls |
|------|-------|------|----------|
| `run_semgrep()` | Untrusted repo checkout | Arbitrary code in Semgrep ruleset scope | Container isolation; non-root user; read-only `contents` in consumer workflows |
| `call_sieve()` | Semgrep JSON + repo alias | Data leak to third party | TLS; documented data minimization in README |
| `post_pr_comment()` | GitHub token + API | Token abuse | Consumer-scoped `GITHUB_TOKEN`; action only creates/updates comments |
| `handle_issue_comment()` | `/sieve` slash commands | Injection via comment body | Strict prefix parsing; no shell execution of comment text |
| Release pipeline | Tags, metadata, digests | Supply-chain tampering | Metadata validation; Cosign signing; branch protection on `main` |

### External entry points

- GitHub `pull_request` and `issue_comment` webhook events
- Sieve API (`sieve.fendora.io`) — outbound only
- GitHub REST API — outbound only
- Container image pull from GHCR — inbound to consumer runners

### Trust assumptions

Attackers are assumed to control PR branch content in consumer repositories. They are **not** assumed to control `fendora-io/sieve-action` releases, maintainer accounts, or org secrets.
