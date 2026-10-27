??? pqb-faq "What is PQBlocks?"

    PQBlocks is an open-source engineering organisation that builds the components of a post-quantum migration as independent packages: post-quantum cryptography (ML-KEM, ML-DSA, SLH-DSA and hybrid modes), migration tooling (crypto inventory, CBOMs, readiness scoring, policy gates, CNSA 2.0 evidence), interoperability (TLS, JOSE, wire formats, certificate requests), conformance testing against NIST ACVP vectors, and quantum-inspired optimisation. Each package lives in its own repository under [github.com/PQBlocks](https://github.com/PQBlocks), is licensed Apache-2.0, and ships its tests, benchmarks, primary sources and a verification report. PQBlocks is a QubitRock project.

??? pqb-faq "Which PQBlocks package should I start with?"

    Start by finding the cryptography you already run. [`pqblocks-scan`](packages/scan.md) inventories RSA, elliptic curves, weak hashes and post-quantum algorithms in source code and TLS endpoints, and writes a CycloneDX 1.6 CBOM and a SARIF report. For new code, use [`pqblocks-primitives`](packages/primitives.md) for ML-KEM, ML-DSA and SLH-DSA, [`pqblocks-jose`](packages/jose.md) for post-quantum JWS and JWE tokens, and [`pqblocks-files`](packages/files.md) for file encryption. The [recipes](recipes/index.md) are complete, tested programs for the common tasks.

??? pqb-faq "Are PQBlocks packages FIPS validated?"

    No. PQBlocks packages implement or wire to the NIST standards FIPS 203, 204 and 205 and test against official vectors where those exist, but none of them is a FIPS 140-3 / CMVP validated cryptographic module, and none claims to be. If you need a validated module, use one, and treat PQBlocks components as the integration, inventory and verification layer around it.

??? pqb-faq "What is post-quantum cryptography?"

    Post-quantum cryptography (PQC) is public-key cryptography designed to stay secure against an attacker with a large quantum computer. It runs on today's ordinary computers. NIST standardised the first algorithms in August 2024: ML-KEM (FIPS 203) for key establishment, and ML-DSA (FIPS 204) and SLH-DSA (FIPS 205) for digital signatures. They replace RSA, Diffie–Hellman and elliptic-curve cryptography, which Shor's algorithm would break.

??? pqb-faq "When do we need to migrate to post-quantum cryptography?"

    Now, for planning and inventory. NIST's transition guidance (NIST IR 8547, draft) deprecates 112-bit quantum-vulnerable algorithms such as RSA-2048 and P-256 after 2030 and disallows all quantum-vulnerable public-key algorithms after 2035. The NSA's CNSA 2.0 asks national security systems to prefer post-quantum algorithms from 2025 for software signing and web services and to use them exclusively between 2030 and 2033 depending on the system type. See the [transition map](transition-map.md) for the dates and sources.

??? pqb-faq "Should I use hybrid or pure post-quantum cryptography?"

    During the transition, hybrid is the safer default: combine ML-KEM with X25519 for key establishment and pair ML-DSA with Ed25519 for signatures. An attacker then has to break both the lattice scheme and the classical one, which protects you if either has an implementation flaw or an unexpected cryptanalytic result. TLS 1.3 already uses the hybrid group X25519MLKEM768. Requirements such as CNSA 2.0 eventually call for post-quantum algorithms on their own, so prefer designs where a policy setting moves you from hybrid to pure.

??? pqb-faq "How do AI coding assistants use PQBlocks?"

    Add the [`pqblocks-mcp`](ai/mcp.md) server to Claude Code, Cursor or any MCP client. It recommends a package for a task, returns its install line and a quickstart executed against the real package, and flags quantum-vulnerable algorithms in pasted code. The [Claude skill and Cursor rules](ai/skills.md) give the same guidance without a server, and [`llms.txt`](llms.txt) and [`llms-full.txt`](llms-full.txt) give agents the whole catalog in one file.

[All questions](faq.md){ .md-button }
