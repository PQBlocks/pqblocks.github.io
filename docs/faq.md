---
title: "Post-quantum cryptography FAQ"
description: "Answers about PQBlocks and the post-quantum transition: what to migrate and when, ML-KEM and ML-DSA, hybrid modes, CBOMs, TLS, installation, validation\u2026"
schema: {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What is PQBlocks?", "acceptedAnswer": {"@type": "Answer", "text": "PQBlocks is an open-source engineering organisation that builds the components of a post-quantum migration as independent packages: post-quantum cryptography (ML-KEM, ML-DSA, SLH-DSA and hybrid modes), migration tooling (crypto inventory, CBOMs, readiness scoring, policy gates, CNSA 2.0 evidence), interoperability (TLS, JOSE, wire formats, certificate requests), conformance testing against NIST ACVP vectors, and quantum-inspired optimisation. Each package lives in its own repository under github.com/PQBlocks, is licensed Apache-2.0, and ships its tests, benchmarks, primary sources and a verification report. PQBlocks is a QubitRock project."}}, {"@type": "Question", "name": "Which PQBlocks package should I start with?", "acceptedAnswer": {"@type": "Answer", "text": "Start by finding the cryptography you already run. pqblocks-scan inventories RSA, elliptic curves, weak hashes and post-quantum algorithms in source code and TLS endpoints, and writes a CycloneDX 1.6 CBOM and a SARIF report. For new code, use pqblocks-primitives for ML-KEM, ML-DSA and SLH-DSA, pqblocks-jose for post-quantum JWS and JWE tokens, and pqblocks-files for file encryption. The recipes are complete, tested programs for the common tasks."}}, {"@type": "Question", "name": "How do I install PQBlocks packages?", "acceptedAnswer": {"@type": "Answer", "text": "Each package installs on its own with pip. Packages already on PyPI install with pip install pqblocks-<name>; the rest install from their GitHub repository with pip install git+https://github.com/PQBlocks/<repository> while their PyPI release is staged. Every package page shows the exact command that works today. Packages that use post-quantum primitives need the liboqs shared library; their README explains how it is found."}}, {"@type": "Question", "name": "Are PQBlocks packages production-ready?", "acceptedAnswer": {"@type": "Answer", "text": "They are pre-1.0 alpha releases. They follow the NIST standards, test against official vectors where those exist and document their limits, but their APIs may still change between minor versions and none has had an external security audit. Treat them as you would any young security library: pin versions, read each package's SECURITY_NOTES.md and VERIFICATION_REPORT.md, and review the code paths you depend on."}}, {"@type": "Question", "name": "Are PQBlocks packages FIPS validated?", "acceptedAnswer": {"@type": "Answer", "text": "No. PQBlocks packages implement or wire to the NIST standards FIPS 203, 204 and 205 and test against official vectors where those exist, but none of them is a FIPS 140-3 / CMVP validated cryptographic module, and none claims to be. If you need a validated module, use one, and treat PQBlocks components as the integration, inventory and verification layer around it."}}, {"@type": "Question", "name": "What licence are PQBlocks packages under?", "acceptedAnswer": {"@type": "Answer", "text": "Apache License 2.0, for every package, the MCP server, the agent skills and this site. You can use, modify and redistribute them commercially. Each algorithm cites its standard or paper in the package's EVIDENCE.md."}}, {"@type": "Question", "name": "What is post-quantum cryptography?", "acceptedAnswer": {"@type": "Answer", "text": "Post-quantum cryptography (PQC) is public-key cryptography designed to stay secure against an attacker with a large quantum computer. It runs on today's ordinary computers. NIST standardised the first algorithms in August 2024: ML-KEM (FIPS 203) for key establishment, and ML-DSA (FIPS 204) and SLH-DSA (FIPS 205) for digital signatures. They replace RSA, Diffie–Hellman and elliptic-curve cryptography, which Shor's algorithm would break."}}, {"@type": "Question", "name": "What does \"harvest now, decrypt later\" mean?", "acceptedAnswer": {"@type": "Answer", "text": "It is the attack in which encrypted traffic or files are recorded today and decrypted years later, once a cryptographically relevant quantum computer exists. It is why key establishment (TLS sessions, VPNs, encrypted archives) has to move to post-quantum algorithms before such a machine is built: data with a long confidentiality life is already exposed. Signatures are not harvested this way, but long-lived keys and trust anchors take years to replace."}}, {"@type": "Question", "name": "When do we need to migrate to post-quantum cryptography?", "acceptedAnswer": {"@type": "Answer", "text": "Now, for planning and inventory. NIST's transition guidance (NIST IR 8547, draft) deprecates 112-bit quantum-vulnerable algorithms such as RSA-2048 and P-256 after 2030 and disallows all quantum-vulnerable public-key algorithms after 2035. The NSA's CNSA 2.0 asks national security systems to prefer post-quantum algorithms from 2025 for software signing and web services and to use them exclusively between 2030 and 2033 depending on the system type. See the transition map for the dates and sources."}}, {"@type": "Question", "name": "What are ML-KEM, ML-DSA and SLH-DSA?", "acceptedAnswer": {"@type": "Answer", "text": "They are the three NIST post-quantum standards published in August 2024. ML-KEM (FIPS 203, formerly Kyber) is a lattice-based key-encapsulation mechanism for agreeing on shared secrets. ML-DSA (FIPS 204, formerly Dilithium) is a lattice-based signature scheme. SLH-DSA (FIPS 205, formerly SPHINCS+) is a hash-based signature scheme with larger signatures and very conservative security assumptions. See the glossary for sizes and related terms."}}, {"@type": "Question", "name": "Should I use hybrid or pure post-quantum cryptography?", "acceptedAnswer": {"@type": "Answer", "text": "During the transition, hybrid is the safer default: combine ML-KEM with X25519 for key establishment and pair ML-DSA with Ed25519 for signatures. An attacker then has to break both the lattice scheme and the classical one, which protects you if either has an implementation flaw or an unexpected cryptanalytic result. TLS 1.3 already uses the hybrid group X25519MLKEM768. Requirements such as CNSA 2.0 eventually call for post-quantum algorithms on their own, so prefer designs where a policy setting moves you from hybrid to pure."}}, {"@type": "Question", "name": "Does TLS already support post-quantum key exchange?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. TLS 1.3 negotiates the hybrid group X25519MLKEM768, which combines X25519 with ML-KEM-768, and major browsers, CDNs and recent OpenSSL releases support it. Whether your own endpoints use it depends on your TLS library and configuration. pqblocks-tls-interop probes an endpoint, reports the negotiated group and flags downgrades to classical key exchange."}}, {"@type": "Question", "name": "What is a CBOM?", "acceptedAnswer": {"@type": "Answer", "text": "A Cryptography Bill of Materials lists the cryptographic algorithms, keys, protocols and certificates a system uses, in a machine-readable format such as CycloneDX. It is to cryptography what an SBOM is to dependencies, and it is the starting point for planning a post-quantum migration and proving progress. pqblocks-scan produces one from source code, and pqblocks-cbom enriches it with quantum-safety and CNSA 2.0 classifications."}}, {"@type": "Question", "name": "How do I sign JWTs with a post-quantum algorithm in Python?", "acceptedAnswer": {"@type": "Answer", "text": "Use pqblocks-jose: generate a composite ML-DSA-65 + Ed25519 key pair, define a policy that pins the algorithms, sign with encode_jws and verify with decode_jws. Both signatures must verify for the token to be accepted. Expect tokens of about 4.6 KB, since an ML-DSA-65 signature alone is 3,309 bytes. The complete recipe runs as written."}}, {"@type": "Question", "name": "How do I find RSA and elliptic-curve cryptography in my code?", "acceptedAnswer": {"@type": "Answer", "text": "Run pqblocks-scan over the source tree. It parses Python by syntax tree and other languages by pattern, marks each algorithm as quantum-vulnerable or not with its file and line, grades readiness from A to F and writes a CycloneDX 1.6 CBOM and a SARIF report for code scanning. For Python data flow, pqblocks-lint follows keys from where they are made to where they are used. See the audit recipe."}}, {"@type": "Question", "name": "Is the quantum-inspired work cryptography?", "acceptedAnswer": {"@type": "Answer", "text": "No. The quantum-inspired packages are classical optimisation algorithms (simulated bifurcation, simulated and simulated-quantum annealing, population annealing, digital-annealer-style search and quantum-inspired evolutionary algorithms) for QUBO and Ising problems such as Max-Cut, scheduling and portfolio selection. They run on ordinary CPUs, make no security claims and are kept in their own area so they are never mistaken for cryptography."}}, {"@type": "Question", "name": "How do AI coding assistants use PQBlocks?", "acceptedAnswer": {"@type": "Answer", "text": "Add the pqblocks-mcp server to Claude Code, Cursor or any MCP client. It recommends a package for a task, returns its install line and a quickstart executed against the real package, and flags quantum-vulnerable algorithms in pasted code. The Claude skill and Cursor rules give the same guidance without a server, and llms.txt and llms-full.txt give agents the whole catalog in one file."}}, {"@type": "Question", "name": "How do I report a security vulnerability?", "acceptedAnswer": {"@type": "Answer", "text": "Privately, through GitHub private vulnerability reporting on the affected repository (https://github.com/PQBlocks/<repository>/security/advisories/new). Do not open a public issue. Reports are acknowledged within 3 working days, assessed within 10, and normally fixed and disclosed within 90 days in agreement with the reporter. See security posture."}}, {"@type": "Question", "name": "How is PQBlocks different from liboqs?", "acceptedAnswer": {"@type": "Answer", "text": "liboqs, from the Open Quantum Safe project, is a C library of post-quantum algorithms. PQBlocks builds on top of maintained implementations like it rather than replacing them. It adds what a migration needs around the primitives: hybrid modes and safe defaults, JOSE tokens and file encryption, crypto inventory and CBOMs, policy gates, TLS checks, NIST ACVP conformance runs and compliance evidence, each as an installable Python package with tests and documentation."}}, {"@type": "Question", "name": "Is PQBlocks free to use commercially?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Every package is released under the Apache License 2.0, which allows commercial use, modification and redistribution, with no usage limits or registration. Keep the licence and notice files when you redistribute the code."}}, {"@type": "Question", "name": "Which languages and platforms does PQBlocks support?", "acceptedAnswer": {"@type": "Answer", "text": "Today, Python 3.11 and newer on Linux, with packages installed from PyPI or GitHub. Packages that use post-quantum primitives need the liboqs shared library. npm modules for JavaScript and TypeScript, native SDKs and framework adapters are on the roadmap; this site lists only what is available now."}}, {"@type": "Question", "name": "How long does a post-quantum migration take?", "acceptedAnswer": {"@type": "Answer", "text": "For a large organisation, years. Inventory alone can take months, because cryptography hides in libraries, protocols, devices and vendor products. That is why the guidance starts now while deadlines run to 2030 and 2035: find what you have, protect long-lived data first with hybrid key establishment, make systems crypto-agile so later changes are configuration, and verify each step."}}, {"@type": "Question", "name": "How do I contribute to PQBlocks?", "acceptedAnswer": {"@type": "Answer", "text": "Open an issue or pull request on the relevant repository under github.com/PQBlocks, following the contributing guide. Every change to cryptographic code must follow the cryptography policy: no novel cryptography, official vectors as the reference, and no overclaiming."}}]}
---
<!-- GENERATED by scripts/gen_docs.py from data/catalog.json - do not edit by hand -->


# Frequently asked questions

<p class="pqb-lead">23 short, direct answers about PQBlocks and the post-quantum transition, each with links to the page that goes deeper.</p>

<div class="grid cards pqb-faq-index" markdown>

-   __[PQBlocks](#pqblocks)__

    ---

    What is PQBlocks · Which PQBlocks package should I start with · How do I install PQBlocks packages …

-   __[The post-quantum transition](#the-post-quantum-transition)__

    ---

    What is post-quantum cryptography · What does "harvest now, decrypt later" mean · When do we need to migrate to post-quantum cryptography …

-   __[Using the packages](#using-the-packages)__

    ---

    How do I sign JWTs with a post-quantum algorithm in Python · How do I find RSA and elliptic-curve cryptography in my code · Is the quantum-inspired work cryptography …

-   __[Comparisons and scope](#comparisons-and-scope)__

    ---

    How is PQBlocks different from liboqs · Is PQBlocks free to use commercially · Which languages and platforms does PQBlocks support …

</div>

## PQBlocks

### What is PQBlocks?

<div class="pqb-answer" markdown>

PQBlocks is an open-source engineering organisation that builds the components of a post-quantum migration as independent packages: post-quantum cryptography (ML-KEM, ML-DSA, SLH-DSA and hybrid modes), migration tooling (crypto inventory, CBOMs, readiness scoring, policy gates, CNSA 2.0 evidence), interoperability (TLS, JOSE, wire formats, certificate requests), conformance testing against NIST ACVP vectors, and quantum-inspired optimisation. Each package lives in its own repository under [github.com/PQBlocks](https://github.com/PQBlocks), is licensed Apache-2.0, and ships its tests, benchmarks, primary sources and a verification report. PQBlocks is a QubitRock project.

</div>

### Which PQBlocks package should I start with?

<div class="pqb-answer" markdown>

Start by finding the cryptography you already run. [`pqblocks-scan`](packages/scan.md) inventories RSA, elliptic curves, weak hashes and post-quantum algorithms in source code and TLS endpoints, and writes a CycloneDX 1.6 CBOM and a SARIF report. For new code, use [`pqblocks-primitives`](packages/primitives.md) for ML-KEM, ML-DSA and SLH-DSA, [`pqblocks-jose`](packages/jose.md) for post-quantum JWS and JWE tokens, and [`pqblocks-files`](packages/files.md) for file encryption. The [recipes](recipes/index.md) are complete, tested programs for the common tasks.

</div>

### How do I install PQBlocks packages?

<div class="pqb-answer" markdown>

Each package installs on its own with pip. Packages already on PyPI install with `pip install pqblocks-<name>`; the rest install from their GitHub repository with `pip install git+https://github.com/PQBlocks/<repository>` while their PyPI release is staged. Every package page shows the exact command that works today. Packages that use post-quantum primitives need the [liboqs](https://openquantumsafe.org/liboqs/) shared library; their README explains how it is found.

</div>

### Are PQBlocks packages production-ready?

<div class="pqb-answer" markdown>

They are pre-1.0 alpha releases. They follow the NIST standards, test against official vectors where those exist and document their limits, but their APIs may still change between minor versions and none has had an external security audit. Treat them as you would any young security library: pin versions, read each package's `SECURITY_NOTES.md` and `VERIFICATION_REPORT.md`, and review the code paths you depend on.

</div>

### Are PQBlocks packages FIPS validated?

<div class="pqb-answer" markdown>

No. PQBlocks packages implement or wire to the NIST standards FIPS 203, 204 and 205 and test against official vectors where those exist, but none of them is a FIPS 140-3 / CMVP validated cryptographic module, and none claims to be. If you need a validated module, use one, and treat PQBlocks components as the integration, inventory and verification layer around it.

</div>

### What licence are PQBlocks packages under?

<div class="pqb-answer" markdown>

Apache License 2.0, for every package, the MCP server, the agent skills and this site. You can use, modify and redistribute them commercially. Each algorithm cites its standard or paper in the package's `EVIDENCE.md`.

</div>

## The post-quantum transition

### What is post-quantum cryptography?

<div class="pqb-answer" markdown>

Post-quantum cryptography (PQC) is public-key cryptography designed to stay secure against an attacker with a large quantum computer. It runs on today's ordinary computers. NIST standardised the first algorithms in August 2024: ML-KEM (FIPS 203) for key establishment, and ML-DSA (FIPS 204) and SLH-DSA (FIPS 205) for digital signatures. They replace RSA, Diffie–Hellman and elliptic-curve cryptography, which Shor's algorithm would break.

</div>

### What does "harvest now, decrypt later" mean?

<div class="pqb-answer" markdown>

It is the attack in which encrypted traffic or files are recorded today and decrypted years later, once a cryptographically relevant quantum computer exists. It is why key establishment (TLS sessions, VPNs, encrypted archives) has to move to post-quantum algorithms before such a machine is built: data with a long confidentiality life is already exposed. Signatures are not harvested this way, but long-lived keys and trust anchors take years to replace.

</div>

### When do we need to migrate to post-quantum cryptography?

<div class="pqb-answer" markdown>

Now, for planning and inventory. NIST's transition guidance (NIST IR 8547, draft) deprecates 112-bit quantum-vulnerable algorithms such as RSA-2048 and P-256 after 2030 and disallows all quantum-vulnerable public-key algorithms after 2035. The NSA's CNSA 2.0 asks national security systems to prefer post-quantum algorithms from 2025 for software signing and web services and to use them exclusively between 2030 and 2033 depending on the system type. See the [transition map](transition-map.md) for the dates and sources.

</div>

### What are ML-KEM, ML-DSA and SLH-DSA?

<div class="pqb-answer" markdown>

They are the three NIST post-quantum standards published in August 2024. ML-KEM (FIPS 203, formerly Kyber) is a lattice-based key-encapsulation mechanism for agreeing on shared secrets. ML-DSA (FIPS 204, formerly Dilithium) is a lattice-based signature scheme. SLH-DSA (FIPS 205, formerly SPHINCS+) is a hash-based signature scheme with larger signatures and very conservative security assumptions. See the [glossary](glossary.md) for sizes and related terms.

</div>

### Should I use hybrid or pure post-quantum cryptography?

<div class="pqb-answer" markdown>

During the transition, hybrid is the safer default: combine ML-KEM with X25519 for key establishment and pair ML-DSA with Ed25519 for signatures. An attacker then has to break both the lattice scheme and the classical one, which protects you if either has an implementation flaw or an unexpected cryptanalytic result. TLS 1.3 already uses the hybrid group X25519MLKEM768. Requirements such as CNSA 2.0 eventually call for post-quantum algorithms on their own, so prefer designs where a policy setting moves you from hybrid to pure.

</div>

### Does TLS already support post-quantum key exchange?

<div class="pqb-answer" markdown>

Yes. TLS 1.3 negotiates the hybrid group X25519MLKEM768, which combines X25519 with ML-KEM-768, and major browsers, CDNs and recent OpenSSL releases support it. Whether your own endpoints use it depends on your TLS library and configuration. [`pqblocks-tls-interop`](packages/tls-interop.md) probes an endpoint, reports the negotiated group and flags downgrades to classical key exchange.

</div>

### What is a CBOM?

<div class="pqb-answer" markdown>

A Cryptography Bill of Materials lists the cryptographic algorithms, keys, protocols and certificates a system uses, in a machine-readable format such as CycloneDX. It is to cryptography what an SBOM is to dependencies, and it is the starting point for planning a post-quantum migration and proving progress. [`pqblocks-scan`](packages/scan.md) produces one from source code, and [`pqblocks-cbom`](packages/cbom.md) enriches it with quantum-safety and CNSA 2.0 classifications.

</div>

## Using the packages

### How do I sign JWTs with a post-quantum algorithm in Python?

<div class="pqb-answer" markdown>

Use [`pqblocks-jose`](packages/jose.md): generate a composite ML-DSA-65 + Ed25519 key pair, define a policy that pins the algorithms, sign with `encode_jws` and verify with `decode_jws`. Both signatures must verify for the token to be accepted. Expect tokens of about 4.6 KB, since an ML-DSA-65 signature alone is 3,309 bytes. The [complete recipe](recipes/jwt-ml-dsa.md) runs as written.

</div>

### How do I find RSA and elliptic-curve cryptography in my code?

<div class="pqb-answer" markdown>

Run [`pqblocks-scan`](packages/scan.md) over the source tree. It parses Python by syntax tree and other languages by pattern, marks each algorithm as quantum-vulnerable or not with its file and line, grades readiness from A to F and writes a CycloneDX 1.6 CBOM and a SARIF report for code scanning. For Python data flow, [`pqblocks-lint`](packages/lint.md) follows keys from where they are made to where they are used. See [the audit recipe](recipes/crypto-audit.md).

</div>

### Is the quantum-inspired work cryptography?

<div class="pqb-answer" markdown>

No. The quantum-inspired packages are classical optimisation algorithms (simulated bifurcation, simulated and simulated-quantum annealing, population annealing, digital-annealer-style search and quantum-inspired evolutionary algorithms) for QUBO and Ising problems such as Max-Cut, scheduling and portfolio selection. They run on ordinary CPUs, make no security claims and are kept in their own area so they are never mistaken for cryptography.

</div>

### How do AI coding assistants use PQBlocks?

<div class="pqb-answer" markdown>

Add the [`pqblocks-mcp`](ai/mcp.md) server to Claude Code, Cursor or any MCP client. It recommends a package for a task, returns its install line and a quickstart executed against the real package, and flags quantum-vulnerable algorithms in pasted code. The [Claude skill and Cursor rules](ai/skills.md) give the same guidance without a server, and [`llms.txt`](llms.txt) and [`llms-full.txt`](llms-full.txt) give agents the whole catalog in one file.

</div>

### How do I report a security vulnerability?

<div class="pqb-answer" markdown>

Privately, through GitHub private vulnerability reporting on the affected repository (`https://github.com/PQBlocks/<repository>/security/advisories/new`). Do not open a public issue. Reports are acknowledged within 3 working days, assessed within 10, and normally fixed and disclosed within 90 days in agreement with the reporter. See [security posture](security/security-notes.md).

</div>

## Comparisons and scope

### How is PQBlocks different from liboqs?

<div class="pqb-answer" markdown>

liboqs, from the Open Quantum Safe project, is a C library of post-quantum algorithms. PQBlocks builds on top of maintained implementations like it rather than replacing them. It adds what a migration needs around the primitives: hybrid modes and safe defaults, JOSE tokens and file encryption, crypto inventory and CBOMs, policy gates, TLS checks, NIST ACVP conformance runs and compliance evidence, each as an installable Python package with tests and documentation.

</div>

### Is PQBlocks free to use commercially?

<div class="pqb-answer" markdown>

Yes. Every package is released under the Apache License 2.0, which allows commercial use, modification and redistribution, with no usage limits or registration. Keep the licence and notice files when you redistribute the code.

</div>

### Which languages and platforms does PQBlocks support?

<div class="pqb-answer" markdown>

Today, Python 3.11 and newer on Linux, with packages installed from PyPI or GitHub. Packages that use post-quantum primitives need the liboqs shared library. npm modules for JavaScript and TypeScript, native SDKs and framework adapters are on the [roadmap](about.md#roadmap); this site lists only what is available now.

</div>

### How long does a post-quantum migration take?

<div class="pqb-answer" markdown>

For a large organisation, years. Inventory alone can take months, because cryptography hides in libraries, protocols, devices and vendor products. That is why the guidance starts now while deadlines run to 2030 and 2035: find what you have, protect long-lived data first with hybrid key establishment, make systems crypto-agile so later changes are configuration, and verify each step.

</div>

### How do I contribute to PQBlocks?

<div class="pqb-answer" markdown>

Open an issue or pull request on the relevant repository under [github.com/PQBlocks](https://github.com/PQBlocks), following the [contributing guide](https://github.com/PQBlocks/.github/blob/main/CONTRIBUTING.md). Every change to cryptographic code must follow the [cryptography policy](https://github.com/PQBlocks/.github/blob/main/CRYPTO-POLICY.md): no novel cryptography, official vectors as the reference, and no overclaiming.

</div>
