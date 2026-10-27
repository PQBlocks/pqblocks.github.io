---
title: Security posture and limits
description: PQBlocks cryptography rules, audit and validation status, constant-time and randomness posture, supported versions and private vulnerability reporting.
---

# Security posture and limits

<p class="pqb-lead">Honest caveats build expert trust. These rules apply to every PQBlocks package; each package's <code>SECURITY_NOTES.md</code> adds its own specifics.</p>

## Cryptography rules

Every package follows the organisation's [cryptography policy](https://github.com/PQBlocks/.github/blob/main/CRYPTO-POLICY.md). A contribution that breaks a rule is not merged.

1. **No novel cryptography.** Only standardised or peer-reviewed algorithms: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) and established classical primitives.
2. **Prefer audited implementations.** Bind to maintained libraries such as liboqs and pyca/cryptography rather than re-implementing primitives.
3. **Hybrid by default.** Combine post-quantum and classical algorithms where the protocol allows. Downgrade to classical-only must be explicit, never silent.
4. **Official vectors are the reference.** NIST ACVP / KAT and Wycheproof vectors, vendored byte-for-byte with source and hash.
5. **Secrets stay secret.** No secret material in logs, exceptions or `repr`. Key and nonce randomness comes from the operating system CSPRNG.
6. **Fail loudly.** Malformed or hostile input is rejected with a typed error before any cryptographic operation.
7. **No overclaiming.** Never "certified", "FIPS-validated", "unbreakable" or "quantum-proof".
8. **Disclose limits.** Constant-time behaviour, side-channel posture and audit status are written down per package.

## Status at a glance

| Property | Status |
|---|---|
| **Validation** | No package is FIPS 140-3 / CMVP validated, and none claims to be. |
| **External audit** | Not yet externally audited. Packages are self-verified; see each `VERIFICATION_REPORT.md`. |
| **Maturity** | 0.x alpha. APIs may change between minor versions. |
| **Primitives** | Post-quantum algorithms come from maintained implementations (liboqs); classical ones from pyca/cryptography. |
| **Constant-time** | Inherited from the underlying implementation for primitive operations. Python glue code is not constant-time. Each package documents its status. |
| **Side channels** | Power and electromagnetic side-channel defences are out of scope for these software packages. |
| **Quantum-inspired packages** | Optimisation algorithms only. No security properties are claimed. |

## Supported versions

During the 0.x series only the latest minor release of each package receives security fixes.

## Reporting a vulnerability

Report suspected vulnerabilities **privately** with GitHub private vulnerability reporting on the affected repository:

```text
https://github.com/PQBlocks/<repository>/security/advisories/new
```

Do not open a public issue, discussion or pull request. Include the package and version, a description and impact, a minimal reproduction and any suggested fix.

| Step | Target |
|---|---|
| Acknowledgement | within 3 working days |
| Initial assessment and severity | within 10 working days |
| Fix and coordinated disclosure | normally within 90 days, agreed with the reporter |

Reporters are credited in the advisory and release notes unless they ask to stay anonymous. Vulnerabilities in upstream libraries such as liboqs or pyca/cryptography should be reported upstream. The full policy is in [SECURITY.md](https://github.com/PQBlocks/.github/blob/main/SECURITY.md).
