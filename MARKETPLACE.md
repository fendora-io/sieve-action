## How it works

Sieve runs on every pull request and uses a trained ML model to separate real vulnerabilities from false positives — so your team only sees findings worth fixing.

1. Sieve scans your PR automatically
2. An ML classifier scores each finding by likelihood of being a real vulnerability
3. False positives are suppressed automatically
4. Each finding gets its own comment — react 👍 (real) or 👎 (false positive) to improve the model

## Setup

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
      - uses: fendora-io/sieve-action@v1.4.0
```

No API keys. No configuration. That's it.

## What you get

- **Less noise** — the model is trained on thousands of labeled findings from real-world repos
- **Per-finding feedback** — react directly on each flagged finding in the PR
- **Privacy first** — raw source code is never stored; only anonymised metadata
- **EU servers** — all data processed on Hetzner infrastructure in Germany

## Data & Privacy

Sieve sends finding metadata to `sieve.fendora.io` for analysis. Raw source files and raw file paths are never stored.

Full details: [Privacy Policy](https://fendora.io/en/privacy)

---

Built by [Fendora](https://fendora.io) · Berlin, Germany · contact@fendora.io
