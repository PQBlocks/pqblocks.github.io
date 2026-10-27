---
title: PQBlocks · Verified building blocks for the post-quantum era
description: Open-source post-quantum engineering. ML-KEM and ML-DSA cryptography, crypto inventory and CBOMs, protocol interoperability, NIST conformance and quantum-inspired optimisation, each package tested and documented.
schema: {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What is PQBlocks?", "acceptedAnswer": {"@type": "Answer", "text": "PQBlocks is an open-source engineering organisation that builds the components of a post-quantum migration as independent packages: post-quantum cryptography (ML-KEM, ML-DSA, SLH-DSA and hybrid modes), migration tooling (crypto inventory, CBOMs, readiness scoring, policy gates, CNSA 2.0 evidence), interoperability (TLS, JOSE, wire formats, certificate requests), conformance testing against NIST ACVP vectors, and quantum-inspired optimisation. Each package lives in its own repository under github.com/PQBlocks, is licensed Apache-2.0, and ships its tests, benchmarks, primary sources and a verification report. PQBlocks is a QubitRock project."}}, {"@type": "Question", "name": "Which PQBlocks package should I start with?", "acceptedAnswer": {"@type": "Answer", "text": "Start by finding the cryptography you already run. pqblocks-scan inventories RSA, elliptic curves, weak hashes and post-quantum algorithms in source code and TLS endpoints, and writes a CycloneDX 1.6 CBOM and a SARIF report. For new code, use pqblocks-primitives for ML-KEM, ML-DSA and SLH-DSA, pqblocks-jose for post-quantum JWS and JWE tokens, and pqblocks-files for file encryption. The recipes are complete, tested programs for the common tasks."}}, {"@type": "Question", "name": "Are PQBlocks packages FIPS validated?", "acceptedAnswer": {"@type": "Answer", "text": "No. PQBlocks packages implement or wire to the NIST standards FIPS 203, 204 and 205 and test against official vectors where those exist, but none of them is a FIPS 140-3 / CMVP validated cryptographic module, and none claims to be. If you need a validated module, use one, and treat PQBlocks components as the integration, inventory and verification layer around it."}}, {"@type": "Question", "name": "What is post-quantum cryptography?", "acceptedAnswer": {"@type": "Answer", "text": "Post-quantum cryptography (PQC) is public-key cryptography designed to stay secure against an attacker with a large quantum computer. It runs on today's ordinary computers. NIST standardised the first algorithms in August 2024: ML-KEM (FIPS 203) for key establishment, and ML-DSA (FIPS 204) and SLH-DSA (FIPS 205) for digital signatures. They replace RSA, Diffie–Hellman and elliptic-curve cryptography, which Shor's algorithm would break."}}, {"@type": "Question", "name": "When do we need to migrate to post-quantum cryptography?", "acceptedAnswer": {"@type": "Answer", "text": "Now, for planning and inventory. NIST's transition guidance (NIST IR 8547, draft) deprecates 112-bit quantum-vulnerable algorithms such as RSA-2048 and P-256 after 2030 and disallows all quantum-vulnerable public-key algorithms after 2035. The NSA's CNSA 2.0 asks national security systems to prefer post-quantum algorithms from 2025 for software signing and web services and to use them exclusively between 2030 and 2033 depending on the system type. See the transition map for the dates and sources."}}, {"@type": "Question", "name": "Should I use hybrid or pure post-quantum cryptography?", "acceptedAnswer": {"@type": "Answer", "text": "During the transition, hybrid is the safer default: combine ML-KEM with X25519 for key establishment and pair ML-DSA with Ed25519 for signatures. An attacker then has to break both the lattice scheme and the classical one, which protects you if either has an implementation flaw or an unexpected cryptanalytic result. TLS 1.3 already uses the hybrid group X25519MLKEM768. Requirements such as CNSA 2.0 eventually call for post-quantum algorithms on their own, so prefer designs where a policy setting moves you from hybrid to pure."}}, {"@type": "Question", "name": "How do AI coding assistants use PQBlocks?", "acceptedAnswer": {"@type": "Answer", "text": "Add the pqblocks-mcp server to Claude Code, Cursor or any MCP client. It recommends a package for a task, returns its install line and a quickstart executed against the real package, and flags quantum-vulnerable algorithms in pasted code. The Claude skill and Cursor rules give the same guidance without a server, and llms.txt and llms-full.txt give agents the whole catalog in one file."}}]}
hide:
  - navigation
  - toc
---

<div class="pqb-hero" markdown>

<div class="pqb-hero__text" markdown>

# PQBlocks

**Verified building blocks for the post-quantum transition.**

PQBlocks is an open-source engineering organisation for the post-quantum (PQ) era. It builds the pieces a real migration needs: NIST-standard cryptography in hybrid modes, tools that find and score the cryptography you already run, formats and protocol checks that carry post-quantum data, conformance against official vectors, and quantum-inspired optimisation. Each package lives in its own repository, ships its tests and evidence, and says what it does **not** do.

[Package catalog](packages/index.md){ .md-button .md-button--primary }
[Recipes](recipes/index.md){ .md-button }
[GitHub](https://github.com/PQBlocks){ .md-button }

<p class="pqb-standards" markdown>Built on [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) · [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) · [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final) · [RFC 7748](https://www.rfc-editor.org/rfc/rfc7748) · [RFC 5869](https://www.rfc-editor.org/rfc/rfc5869) · [CycloneDX 1.6](https://cyclonedx.org/specification/overview/) · [NIST ACVP](https://pages.nist.gov/ACVP/)</p>

</div>

<figure class="pqb-hero__figure" markdown>
<div class="pqb-figure pqb-figure--hero" data-figure="lattice" data-label="Pillars on the points of a skewed two-dimensional lattice, the structure behind ML-KEM and ML-DSA. The point closest to the pointer rises, and a path of whole basis steps draws to it from the origin."></div>
<figcaption>A lattice, the mathematics under ML-KEM and ML-DSA. Point anywhere: the closest lattice point answers.</figcaption>
</figure>

</div>

## What is the post-quantum transition?

A cryptographically relevant quantum computer (CRQC) running Shor's algorithm would break RSA, Diffie–Hellman and elliptic-curve cryptography: the public-key algorithms behind TLS, code signing, tokens and encrypted archives. Data recorded today can be decrypted once such a machine exists, which is why the threat is called *harvest now, decrypt later*. In August 2024 NIST published the replacements as final standards: **ML-KEM** (FIPS 203) for key establishment, **ML-DSA** (FIPS 204) and **SLH-DSA** (FIPS 205) for signatures. NIST's transition guidance (NIST IR 8547, draft) deprecates today's 112-bit public-key algorithms after 2030 and disallows them after 2035, and the NSA's CNSA 2.0 sets similar deadlines for national security systems. Changing the algorithm is the small part. The work is finding every use, migrating safely, carrying larger keys through real protocols and proving the result.

## Areas

--8<-- "includes/areas-table.md"

![PQBlocks ecosystem: packages across PQ cryptography, migration and readiness, interoperability, conformance and quantum-inspired optimisation](assets/diagrams/ecosystem-light.svg#only-light)
![PQBlocks ecosystem: packages across PQ cryptography, migration and readiness, interoperability, conformance and quantum-inspired optimisation](assets/diagrams/ecosystem-dark.svg#only-dark)

Coding assistants can use the same catalog through the [MCP server, Claude skill and Cursor rules](ai/index.md).

## Start in a minute

Each tab is the package's own quickstart, executed against the package source before this site was published.

=== "Post-quantum KEM"

    ```python title="ML-KEM-768 with pqblocks-primitives"
    --8<-- "includes/quickstart/primitives.py"
    ```

    [Hybrid X25519 + ML-KEM recipe](recipes/hybrid-kem.md) · [pqblocks-primitives](packages/primitives.md)

=== "Encrypt a file"

    ```python title="ML-KEM-768 + X25519 file encryption with pqblocks-files"
    --8<-- "includes/quickstart/files.py"
    ```

    [Full recipe with key files](recipes/encrypt-files.md) · [pqblocks-files](packages/files.md)

=== "Find RSA and ECC"

    ```python title="Crypto inventory with pqblocks-scan"
    --8<-- "includes/quickstart/scan.py"
    ```

    [Audit recipe](recipes/crypto-audit.md) · [pqblocks-scan](packages/scan.md)

=== "Solve an Ising problem"

    ```python title="Simulated Bifurcation with pqblocks-bifurcation"
    --8<-- "includes/quickstart/bifurcation.py"
    ```

    [Max-Cut recipe](recipes/qubo-maxcut.md) · [pqblocks-bifurcation](packages/bifurcation.md)

## A package for every step of the migration

![Six migration steps (discover, assess, govern, migrate, interoperate, verify) and the PQBlocks packages for each](assets/diagrams/pipeline-light.svg#only-light)
![Six migration steps (discover, assess, govern, migrate, interoperate, verify) and the PQBlocks packages for each](assets/diagrams/pipeline-dark.svg#only-dark)

The [transition map](transition-map.md) walks through each step, the deadlines behind it and the package that does the work.

## How PQBlocks earns trust

- **Standards, not inventions.** Only standardised or peer-reviewed algorithms. Post-quantum primitives come from maintained implementations such as [liboqs](https://openquantumsafe.org/liboqs/).
- **Evidence in every repository.** `TESTING`, `BENCHMARKS`, `EVIDENCE`, `SECURITY_NOTES` and a `VERIFICATION_REPORT`, with benchmarks that include the cases where a package loses. See [how we verify](security/verification-reports.md).
- **Limits stated up front.** Packages are pre-1.0. None is FIPS 140-3 or CMVP validated or externally audited, and none claims to be. See [security posture](security/security-notes.md).
- **Executed documentation.** Every quickstart and recipe on this site is run against the package source before it is published.

## Frequently asked questions

--8<-- "includes/faq-home.md"
