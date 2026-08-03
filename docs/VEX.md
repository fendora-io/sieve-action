# Vulnerability Exploitability eXchange (VEX)

Known dependency vulnerabilities assessed as **not exploitable** in `fendora-io/sieve-action`.

## Suppressions

| CVE / GHSA | Component | Status | Justification | Last reviewed |
|------------|-----------|--------|---------------|---------------|
| PYSEC-2026-2132 | click 8.1.8 (transitive via semgrep) | Not affected | `click.edit()` is not invoked by sieve-action or entrypoint.py; vulnerability requires attacker to control arguments to that API | 2026-07-13 |
| PYSEC-2026-3481 | mcp 1.23.3 (transitive via semgrep) | Not affected | Requires `server.experimental.enable_tasks()` on a multi-client MCP server; sieve-action never runs an MCP server, only invokes `semgrep` as a one-shot CLI scan (entrypoint.py); fix blocked until semgrep allows mcp>=1.27.2 | 2026-08-02 |
| PYSEC-2026-3482 | mcp 1.23.3 (transitive via semgrep) | Not affected | Requires an HTTP (SSE/Streamable) MCP server transport with bearer-token auth; sieve-action never runs an MCP server; fix blocked until semgrep allows mcp>=1.27.2 | 2026-08-02 |
| PYSEC-2026-3483 | mcp 1.23.3 (transitive via semgrep) | Not affected | Requires exposing the deprecated `mcp.server.websocket.websocket_server` transport; sieve-action never runs an MCP server; fix blocked until semgrep allows mcp>=1.28.1 | 2026-08-02 |

## Process

1. `pip-audit`, Dependabot, or CodeQL reports a finding.
2. Maintainers assess exploitability in the action container context.
3. If not exploitable, add a row here before merging a suppression.
4. If exploitable, remediate via dependency update before the next release.

See [SECURITY-SCANNING-POLICY.md](SECURITY-SCANNING-POLICY.md).
