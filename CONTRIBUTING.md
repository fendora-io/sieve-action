# Contributing

Thanks for your interest in improving Sieve.

## How to contribute

1. Fork the repo and create a branch from `main`
2. Sign every commit (`git commit -s`) per the [Developer Certificate of Origin](#developer-certificate-of-origin-dco) below
3. Open a pull request — all changes require at least one approving review from [@fendora-io/legends](https://github.com/orgs/fendora-io/teams/legends) before merge
4. Ensure CI passes (`Validate action.yml`, `Run tests`, `DCO`, `Analyze`, `Semgrep scan`)

We use GitHub pull requests and issues for all contributions.

## Developer Certificate of Origin (DCO)

By contributing, you certify that you have the right to submit your contribution under the project's [Apache 2.0 license](LICENSE), per the [Developer Certificate of Origin](https://developercertificate.org/).

Every commit must include a `Signed-off-by` line:

```bash
git commit -s -m "Describe your change"
```

The DCO check runs on all pull requests.

## Development

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for dependency management, build instructions, and running tests locally.

## Reporting issues

Open a [GitHub issue](https://github.com/fendora-io/sieve-action/issues/new/choose) with:
- What you expected to happen
- What actually happened
- Your workflow file (redact any secrets)

## Security vulnerabilities

Please **do not** report security vulnerabilities in public issues. See [SECURITY.md](SECURITY.md) for our private disclosure process.

## Pull requests

1. Test your change against a real repository when possible
2. Describe what changed and why in the PR description
3. Keep changes focused — avoid unrelated refactors

## Action inputs / outputs

Changes to `action.yml` inputs or outputs are breaking changes for existing users. Discuss in an issue first before submitting a PR that modifies the public interface.

## Contact

For questions: **contact@fendora.io**
