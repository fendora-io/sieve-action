# Vulnerability Exploitability eXchange (VEX)

Known dependency vulnerabilities assessed as **not exploitable** in `fendora-io/sieve-action`.

## Suppressions

| CVE / GHSA | Component | Status | Justification | Last reviewed |
|------------|-----------|--------|---------------|---------------|
| _none_ | — | — | No suppressions at this time | 2026-07-13 |

## Process

1. `pip-audit`, Dependabot, or CodeQL reports a finding.
2. Maintainers assess exploitability in the action container context.
3. If not exploitable, add a row here before merging a suppression.
4. If exploitable, remediate via dependency update before the next release.

See [SECURITY-SCANNING-POLICY.md](SECURITY-SCANNING-POLICY.md).
