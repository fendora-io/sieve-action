# Vulnerability Exploitability eXchange (VEX)

Known dependency vulnerabilities assessed as **not exploitable** in `fendora-io/sieve-action`.

## Suppressions

| CVE / GHSA | Component | Status | Justification | Last reviewed |
|------------|-----------|--------|---------------|---------------|
| PYSEC-2026-2132 | click 8.1.8 (transitive via semgrep) | Not affected | `click.edit()` is not invoked by sieve-action or entrypoint.py; vulnerability requires attacker to control arguments to that API | 2026-07-13 |

## Process

1. `pip-audit`, Dependabot, or CodeQL reports a finding.
2. Maintainers assess exploitability in the action container context.
3. If not exploitable, add a row here before merging a suppression.
4. If exploitable, remediate via dependency update before the next release.

See [SECURITY-SCANNING-POLICY.md](SECURITY-SCANNING-POLICY.md).
