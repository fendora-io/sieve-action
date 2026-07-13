# Governance

## Members with access to sensitive resources

| Member / team | GitHub | Sensitive access |
|---------------|--------|------------------|
| Mohi Jalili | [@mohijalili](https://github.com/mohijalili) | Repository admin, branch protection, GHCR package publish, release signing (Cosign), GitHub Actions secrets |
| Legends | [@fendora-io/legends](https://github.com/orgs/fendora-io/teams/legends) | Pull request review and approval (via [CODEOWNERS](.github/CODEOWNERS)) |

Sensitive resources for this project include: the `fendora-io/sieve-action` repository settings, GitHub Container Registry (`ghcr.io/fendora-io/sieve-action`), release assets, and any repository or organization secrets used by CI/CD.

### Legends team

The [@fendora-io/legends](https://github.com/orgs/fendora-io/teams/legends) team reviews and approves pull requests before merge. Current members:

- [@mohijalili](https://github.com/mohijalili)
- [@djalili](https://github.com/djalili)
- [@malivix](https://github.com/malivix)
- [@RezDev94](https://github.com/RezDev94)
- [@1mohammad](https://github.com/1mohammad)
- [@AliRanjbarzadeh](https://github.com/AliRanjbarzadeh)

## Roles and responsibilities

| Role | Who | Responsibilities |
|------|-----|------------------|
| **Maintainer** | [@mohijalili](https://github.com/mohijalili) | Merge approved PRs; cut semver releases; respond to security reports within 48 hours; manage Dependabot updates; maintain branch protection and required CI checks |
| **Reviewer** | [@fendora-io/legends](https://github.com/orgs/fendora-io/teams/legends) | Review PRs for correctness and security; approve before merge (cannot be the PR author) |
| **Contributor** | Anyone | Open focused PRs with tests where applicable; sign commits per DCO; follow [CONTRIBUTING.md](CONTRIBUTING.md) |

## Decision-making

- Day-to-day changes go through pull requests with at least one approving review from the Legends team.
- Breaking changes to `action.yml` inputs/outputs require discussion in an issue before implementation.
- Security fixes may be expedited but still require review before merge to `main`.

## Contact

General questions: **contact@fendora.io**  
Security issues: **security@fendora.io** (see [SECURITY.md](SECURITY.md))
