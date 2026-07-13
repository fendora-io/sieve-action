# Release Verification

This document describes how to verify the integrity, authenticity, and publisher identity of **Sieve by Fendora** release artifacts.

## Release artifacts

Each official release (`v*`) includes:

| Asset | Identifier | Location |
|-------|------------|----------|
| Container image | `ghcr.io/fendora-io/sieve-action:vX.Y.Z` | GitHub Container Registry |
| Image digest | `sha256:…` | Release workflow output / GHCR |
| Cosign signature | Keyless (Sigstore) | OCI image signature on GHCR |
| Digest attestation | `image-digest.sigstore.json` | [GitHub Release assets](https://github.com/fendora-io/sieve-action/releases) |
| SBOM | `sbom.spdx.json` | GitHub Release assets |

All container images are tagged with the semver release identifier (e.g. `v1.4.3`).

## Verify image integrity and authenticity

### 1. Install Cosign

```bash
brew install cosign   # macOS
```

### 2. Verify the container image signature

```bash
cosign verify ghcr.io/fendora-io/sieve-action:v1.4.3 \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp '^https://github\.com/fendora-io/sieve-action/\.github/workflows/.*'
```

### 3. Verify the release digest attestation

Download `image-digest.sigstore.json` from the GitHub release, then:

```bash
cosign verify-blob \
  --bundle image-digest.sigstore.json \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp '^https://github\.com/fendora-io/sieve-action/\.github/workflows/.*' \
  image-digest.txt
```

## Verify release publisher identity

Release artifacts are signed using **GitHub Actions OIDC** (keyless Sigstore). Cosign verification confirms the signing identity matches this repository's `docker.yml` release workflow at `fendora-io/sieve-action`.

## SBOM

Each release includes `sbom.spdx.json` listing container image components.
