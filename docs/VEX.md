# Vulnerability Exploitability eXchange (VEX)

Known dependency vulnerabilities assessed as **not exploitable** in `fendora-io/sieve-action`.

## Suppressions

None active. `pip-audit` runs in CI without any `--ignore-vuln` flags.

## Resolved

Previously suppressed findings, now fixed by upgrading the dependency. Kept for audit history.

| CVE / GHSA | Component | Resolution | Resolved |
|------------|-----------|------------|----------|
| PYSEC-2026-2132 | click (transitive via semgrep) | Upgraded to click 8.4.2 | 2026-10-11 |
| PYSEC-2026-3481 | mcp (transitive via semgrep) | Upgraded to mcp 1.29.0 | 2026-10-11 |
| PYSEC-2026-3482 | mcp (transitive via semgrep) | Upgraded to mcp 1.29.0 | 2026-10-11 |
| PYSEC-2026-3483 | mcp (transitive via semgrep) | Upgraded to mcp 1.29.0 | 2026-10-11 |
| PYSEC-2026-3552 | cryptography (transitive via semgrep) | Upgraded to cryptography 50.0.2 | 2026-10-11 |

## Process

1. `pip-audit`, Dependabot, or CodeQL reports a finding.
2. Maintainers assess exploitability in the action container context.
3. If not exploitable, add a row here before merging a suppression.
4. If exploitable, remediate via dependency update before the next release.

See [SECURITY-SCANNING-POLICY.md](SECURITY-SCANNING-POLICY.md).
