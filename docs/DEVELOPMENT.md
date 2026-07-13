# Development Guide

## Prerequisites

- Docker (for container builds)
- Python 3.11+ (for local testing)
- [pip-tools](https://pypi.org/project/pip-tools/) (for dependency locking)

## Dependencies

### How dependencies are selected

Direct Python dependencies are declared in [`requirements.in`](../requirements.in):

- `semgrep` — static analysis engine
- `requests` — HTTP client for Sieve and GitHub APIs

The Docker base image is `python:3.11-slim`, pinned by digest in [`Dockerfile`](../Dockerfile).

GitHub Actions and Docker ecosystem dependencies are pinned to commit SHAs in workflow files.

### How dependencies are obtained and locked

1. Edit `requirements.in` with desired package versions.
2. Regenerate the lock file with hashes:

   ```bash
   pip install pip-tools
   pip-compile --generate-hashes --output-file=requirements.txt requirements.in
   ```

3. The Docker build installs from `requirements.txt` with `--require-hashes`.

### How dependencies are tracked

- **[Dependabot](../.github/dependabot.yml)** opens weekly PRs for pip, Docker, and GitHub Actions updates.
- Security findings from **CodeQL** and **Semgrep** run on every PR.
- Release notes are recorded in [`CHANGELOG.md`](../CHANGELOG.md) and [GitHub Releases](https://github.com/fendora-io/sieve-action/releases).

## Building

### Docker image (production path)

```bash
docker build -t sieve-action:local .
```

The release pipeline (`.github/workflows/docker.yml`) builds and pushes to `ghcr.io/fendora-io/sieve-action` on pushes to `main` and version tags (`v*`).

### Local Python (without Docker)

```bash
pip install --require-hashes -r requirements.txt
python3 entrypoint.py
```

Note: Semgrep must be available on `PATH` when running outside Docker.

## Testing

Unit tests use the Python standard library (`unittest`):

```bash
python3 -m unittest discover -s tests -v
```

CI runs tests on every pull request and push to `main` (see `.github/workflows/ci.yml`).

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — system design, actors, data flows
- [SECURITY-ASSESSMENT.md](SECURITY-ASSESSMENT.md) — threat summary
- [GOVERNANCE.md](../GOVERNANCE.md) — maintainers and roles
- [CONTRIBUTING.md](../CONTRIBUTING.md) — contribution and DCO requirements
