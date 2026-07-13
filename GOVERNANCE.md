# Governance

## Members with access to sensitive resources

| Member | GitHub | Sensitive access |
|--------|--------|------------------|
| Mohi Jalili | [@mohijalili](https://github.com/mohijalili) | Repository admin, branch protection, GHCR package publish, release signing (Cosign), GitHub Actions secrets |

Sensitive resources for this project include: the `fendora-io/sieve-action` repository settings, GitHub Container Registry (`ghcr.io/fendora-io/sieve-action`), release assets, and any repository or organization secrets used by CI/CD.

## Roles and responsibilities

| Role | Responsibilities |
|------|----------------|
| **Maintainer** | Merge approved PRs; cut semver releases; respond to security reports within 48 hours; manage Dependabot updates; maintain branch protection and required CI checks |
| **Contributor** | Open focused PRs with tests where applicable; sign commits per DCO; follow [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Reviewer** | Review PRs for correctness and security; approve before merge (cannot be the PR author) |

## Decision-making

- Day-to-day changes go through pull requests with at least one approving review.
- Breaking changes to `action.yml` inputs/outputs require discussion in an issue before implementation.
- Security fixes may be expedited but still require review before merge to `main`.

## Contact

General questions: **contact@fendora.io**  
Security issues: **security@fendora.io** (see [SECURITY.md](SECURITY.md))
