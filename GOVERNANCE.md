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
- **PR authors must not approve their own pull requests.** Reviews must come from a different member of the Legends team.
- Breaking changes to `action.yml` inputs/outputs require discussion in an issue before implementation.
- Security fixes may be expedited but still require review before merge to `main`.

## Escalated permissions (GV-04.01)

Before granting repository **admin**, **maintain**, or **secrets** access to a collaborator:

1. The person must have a track record of merged contributions or a documented business need.
2. An existing maintainer reviews and approves the access change.
3. Access is granted at the lowest level required (prefer team membership over direct admin).
4. Access is recorded in the table above.

Revoke escalated access when no longer needed.

## Contact

General questions: **contact@fendora.io**  
Security issues: **security@fendora.io** (see [SECURITY.md](SECURITY.md))
