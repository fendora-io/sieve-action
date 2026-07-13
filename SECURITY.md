# Security Policy

## Supported Versions

We support the **latest semver release** and the **two prior minor/patch releases** with security fixes.

| Version | Supported | Security fixes until |
|---------|-----------|----------------------|
| v1.4.4  | ✅        | Until v1.5.0 or 6 months after next major, whichever is sooner |
| v1.4.3  | ✅        | Same as above |
| v1.4.2  | ✅        | Same as above |
| < v1.4.2 | ❌        | Upgrade to a supported version |

### End of support

When a release line is no longer supported, it will be listed here and removed from the table above. Users on unsupported versions should upgrade to the latest release.

**Current status:** All listed versions are actively supported. No end-of-support announcements to date.

## Release verification

See [docs/RELEASE-VERIFICATION.md](docs/RELEASE-VERIFICATION.md) for instructions to verify release integrity, authenticity, and publisher identity (Cosign / Sigstore).

## Security scanning

See [docs/SECURITY-SCANNING-POLICY.md](docs/SECURITY-SCANNING-POLICY.md) for SCA/SAST thresholds and [docs/VEX.md](docs/VEX.md) for non-exploitable vulnerability suppressions.

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Report vulnerabilities privately to: **security@fendora.io**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

We aim to respond within 48 hours and will keep you informed throughout the fix process.

## Published security advisories

When we confirm a security vulnerability, we publish a [GitHub Security Advisory](https://github.com/fendora-io/sieve-action/security/advisories) with affected versions, severity, and remediation steps.

No security advisories have been published to date.

## Scope

This policy covers the `fendora-io/sieve-action` repository. For vulnerabilities in the Sieve API service itself, report to the same address.
