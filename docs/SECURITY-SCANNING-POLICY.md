# Security Scanning Policy

SCA and SAST policies for `fendora-io/sieve-action`.

## Secrets and credentials

| Rule | Policy |
|------|--------|
| **Storage** | Never commit secrets. Use GitHub Actions/org secrets for CI only. |
| **Access** | Privileged secrets only in the release signing workflow. |
| **Rotation** | Rotate compromised secrets immediately; review quarterly. |
| **Client IDs** | The Sieve API key in `entrypoint.py` is a public client identifier. |

## SCA — dependency vulnerabilities

### Remediation thresholds

| Severity | On PR | Before release |
|----------|-------|----------------|
| **Critical / High** | Block merge | Must resolve or VEX suppress |
| **Medium** | Fix within 30 days | Should resolve |
| **Low** | Track via Dependabot | Best-effort |

### Automated enforcement

- **`pip-audit`** on every PR/push — fails on High/Critical in `requirements.txt`
- **Dependabot** — weekly pip, Docker, and Actions updates
- **CodeQL** — Python analysis on every PR

Pre-release: no open High/Critical alerts before tagging.

Non-exploitable findings: document in [VEX.md](VEX.md).

## SAST — code security weaknesses

### Remediation thresholds

| Severity | Action |
|----------|--------|
| **Error / High** | Block merge until fixed |
| **Warning / Medium** | Fix before next minor release |
| **Info / Low** | Track in issue |

### Automated enforcement

- **Semgrep** (`p/owasp-top-ten`) — fails on blocking findings every PR
- **CodeQL** — triaged per thresholds above

Last reviewed: **2026-07-13**
