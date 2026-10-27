---
title: PQBlocks · Verified building blocks for the post-quantum era
description: Open-source post-quantum engineering. ML-KEM and ML-DSA cryptography, crypto inventory and CBOMs, protocol interoperability, NIST conformance and quantum-inspired optimisation, each package tested and documented.
hide:
  - navigation
  - toc
---

<div class="pqb-hero" markdown>

<span class="pqb-kicker">Open engineering for the post-quantum era</span>

# Verified building blocks for the post-quantum transition

<p class="pqb-lead" markdown>**PQBlocks is an open-source engineering organisation for the post-quantum (PQ) era.** It builds the components a real migration needs: NIST-standard cryptography (ML-KEM, ML-DSA, SLH-DSA) in hybrid modes, tools that find and score the cryptography you already run, formats and protocol checks that carry post-quantum data, conformance against official NIST vectors, and quantum-inspired optimisation. Every package ships its tests and evidence and states what it does **not** do.</p>

[Browse the packages](packages/index.md){ .md-button .md-button--primary }
[Solve a task](recipes/index.md){ .md-button }
[Connect your AI assistant](ai/index.md){ .md-button }

</div>

<div class="pqb-stats" markdown>
<div><strong>26</strong><span>packages, each its own repository</span></div>
<div><strong>5</strong><span>areas of the PQ transition</span></div>
<div><strong>26 / 26</strong><span>quickstarts executed before publishing</span></div>
<div><strong>9</strong><span>evidence documents per package</span></div>
<div><strong>Open</strong><span>source under Apache-2.0, no usage limits</span></div>
</div>

![PQBlocks ecosystem: 26 packages across PQ cryptography, migration and readiness, interoperability, conformance and quantum-inspired optimisation](assets/diagrams/ecosystem-light.svg#only-light)
![PQBlocks ecosystem: 26 packages across PQ cryptography, migration and readiness, interoperability, conformance and quantum-inspired optimisation](assets/diagrams/ecosystem-dark.svg#only-dark)

## What is the post-quantum transition?

A cryptographically relevant quantum computer (CRQC) running Shor's algorithm would break RSA, Diffie–Hellman and elliptic-curve cryptography: the public-key algorithms behind TLS, code signing, tokens and encrypted archives. Data recorded today can be decrypted once such a machine exists, which is why the threat is called *harvest now, decrypt later*. In August 2024 NIST published the replacements as final standards: **ML-KEM** (FIPS 203) for key establishment, **ML-DSA** (FIPS 204) and **SLH-DSA** (FIPS 205) for signatures. NIST's transition guidance (NIST IR 8547, draft) deprecates today's 112-bit public-key algorithms after 2030 and disallows them after 2035, and the NSA's CNSA 2.0 sets similar deadlines for national security systems. Changing the algorithm is the small part. The work is finding every use, migrating safely, carrying larger keys through real protocols and proving the result.

## Five areas, one ecosystem

<div class="grid cards" markdown>

-   :material-shield-key-outline:{ .lg .middle } __[PQ cryptography](packages/crypto.md)__

    ---

    ML-KEM, ML-DSA and SLH-DSA through maintained implementations, hybrid ML-KEM + X25519 key establishment, composite signatures, post-quantum JOSE and file encryption.

-   :material-radar:{ .lg .middle } __[Migration & readiness](packages/migration.md)__

    ---

    Find RSA and ECC in code and on the wire, emit CycloneDX CBOMs and SARIF, score crypto-agility, gate CI with policy-as-code and build CNSA 2.0 evidence.

-   :material-transit-connection-variant:{ .lg .middle } __[Interoperability](packages/interop.md)__

    ---

    Carry post-quantum data through real protocols: TLS 1.3 X25519MLKEM768 probes, JWE layouts, binary containers and ML-KEM certificate requests.

-   :material-check-decagram-outline:{ .lg .middle } __[Conformance](packages/conformance.md)__

    ---

    Run official NIST ACVP vectors across implementations and reject malformed FIPS 203/204 inputs at the boundary, so correctness is measured.

-   :material-chart-bell-curve-cumulative:{ .lg .middle } __[Quantum-inspired](packages/optimization.md)__

    ---

    Classical solvers modelled on quantum dynamics (simulated bifurcation, annealing families, QIEA) for QUBO and Ising problems. No security claims.

-   :material-robot-outline:{ .lg .middle } __[AI assistants](ai/index.md)__

    ---

    An MCP server, a Claude skill, Cursor rules and `llms.txt`, so coding agents pick the right package and use its real API.

</div>

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

<div class="grid pqb-two" markdown>

!!! success "Standards, not inventions"
    Only standardised or peer-reviewed algorithms. Post-quantum primitives come from maintained implementations such as [liboqs](https://openquantumsafe.org/liboqs/); PQBlocks never invents cryptography.

!!! info "Evidence in every repository"
    Each package ships `TESTING`, `BENCHMARKS`, `EVIDENCE`, `SECURITY_NOTES` and a `VERIFICATION_REPORT`. Benchmarks include the cases where it loses.

!!! warning "Limits stated up front"
    Pre-1.0 packages say so. Nothing here is FIPS 140-3 or CMVP validated, and no package claims to be. Read the [security posture](security/security-notes.md).

!!! abstract "Executed documentation"
    Every quickstart and recipe on this site is run against the package source before it is published. A snippet that does not run is not published.

</div>

## Frequently asked questions

### What is PQBlocks?

PQBlocks is an open-source organisation that builds post-quantum engineering components as independent packages: cryptography (ML-KEM, ML-DSA, SLH-DSA and hybrid modes), migration tooling (crypto inventory, CBOMs, readiness scoring, policy gates, CNSA 2.0 evidence), interoperability (TLS, JOSE, wire formats, certificate requests), conformance testing (NIST ACVP) and quantum-inspired optimisation. Each package lives in its own repository under [github.com/PQBlocks](https://github.com/PQBlocks), is licensed Apache-2.0, and ships tests, benchmarks, primary sources and a verification report. PQBlocks is a QubitRock project.

### Which package should I start with?

Start by finding what you have. [`pqblocks-scan`](packages/scan.md) inventories RSA, ECC, weak hashes and post-quantum algorithms in source code and TLS endpoints and writes a CycloneDX CBOM and SARIF report. For new code, use [`pqblocks-primitives`](packages/primitives.md) for ML-KEM, ML-DSA and SLH-DSA, [`pqblocks-jose`](packages/jose.md) for post-quantum JWS/JWE tokens and [`pqblocks-files`](packages/files.md) for file encryption. The [recipes](recipes/index.md) give complete, tested solutions for the common tasks.

### Should I use hybrid or pure post-quantum cryptography?

During the transition, hybrid is the safer default: combine ML-KEM with X25519 for key establishment, and pair ML-DSA with Ed25519 for signatures. An attacker then has to break both the lattice scheme and the classical one, which protects you if either has an implementation flaw or an unexpected cryptanalytic result. TLS 1.3 deployments already use the hybrid group X25519MLKEM768. Requirements such as CNSA 2.0 eventually call for post-quantum algorithms on their own, so choose packages with a policy setting that can move from hybrid to pure without code changes.

### Are PQBlocks packages FIPS validated?

No. PQBlocks packages implement or wire to the NIST standards (FIPS 203, 204 and 205) and test against official vectors where those exist, but none of them is a FIPS 140-3 / CMVP validated cryptographic module, and none claims to be. If you need a validated module, use one and treat PQBlocks components as the integration, inventory and verification layer around it. Each package's `SECURITY_NOTES.md` states its audit and constant-time status.

### Is the quantum-inspired work cryptography?

No. The quantum-inspired packages are classical optimisation algorithms (simulated bifurcation, simulated and simulated-quantum annealing, population annealing, digital-annealer-style search, quantum-inspired evolutionary algorithms) for QUBO and Ising problems such as Max-Cut, scheduling and portfolio selection. They run on ordinary CPUs, make no security claims, and are kept in their own area so they are never mistaken for cryptography.

### How do AI coding assistants use PQBlocks?

Add the [`pqblocks-mcp`](ai/mcp.md) server to Claude Code, Cursor or any MCP client. It recommends a package for a task, returns its install line and a quickstart executed against the real package, and flags quantum-vulnerable algorithms in pasted code. The [Claude skill and Cursor rules](ai/skills.md) give the same guidance without a server, and [`llms.txt`](llms.txt) and [`llms-full.txt`](llms-full.txt) give agents the whole catalog in one file.
