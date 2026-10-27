# Security Notes & Caveats

Honest caveats build expert trust. Every PQBlocks repository states its cryptographic limitations plainly.

## Cryptographic Posture

| Property | Status | Details |
|---|---|---|
| **Constant-Time Execution** | Partial | Core polynomial multiplications and secret key operations wrap audited C implementations (`liboqs`). Higher-level Python/JS glue code is **not** constant-time. Do not expose decapsulation routines to untrusted network timing side-channels without blinding. |
| **Side-Channel Protections** | Baseline | Algorithms defend against software-based timing leaks in core routines. Power analysis (DPA/SPA) and electromagnetic side-channel defenses are not implemented. |
| **Random Number Generation** | OS-Backed | Entropy is exclusively sourced from the operating system CSPRNG (`os.urandom` / `crypto.getRandomValues`). Custom or user-seeded PRNGs are strictly prohibited in production routines. |
| **External Audits** | Self-Verified | Packages are self-verified against NIST ACVP vectors and rigorous automated test benches. They have not undergone third-party commercial cryptographic audits. |

## Reporting Vulnerabilities

Security issues should be reported directly via **GitHub Private Vulnerability Reporting** on the affected repository:
- Acknowledgement within 3 business days.
- Coordinated vulnerability disclosure normally within 90 days.
- For emergency security contact: `security@pqblocks.org`.
