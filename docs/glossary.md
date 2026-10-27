---
title: "Post-quantum glossary"
description: "Plain definitions of post-quantum terms: ML-KEM, ML-DSA, SLH-DSA, hybrid key exchange, X25519MLKEM768, CBOM, CNSA 2.0, NIST IR 8547, ACVP, QUBO and more."
schema: {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "PQBlocks post-quantum glossary", "url": "https://pqblocks.github.io/glossary/", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": "Post-quantum cryptography (PQC)", "description": "Post-quantum cryptography is public-key cryptography designed to resist attacks by large quantum computers while running on ordinary computers. The first NIST standards are ML-KEM, ML-DSA and SLH-DSA.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Cryptographically relevant quantum computer (CRQC)", "description": "A cryptographically relevant quantum computer is a quantum computer large and reliable enough to run Shor's algorithm against real RSA and elliptic-curve keys. None is known to exist; migration deadlines are set so systems move before one does.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Shor's algorithm", "description": "Shor's algorithm is a quantum algorithm that factors integers and computes discrete logarithms in polynomial time, which breaks RSA, Diffie–Hellman, DSA and elliptic-curve cryptography.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Grover's algorithm", "description": "Grover's algorithm is a quantum search algorithm with a quadratic speed-up. It roughly halves the effective strength of symmetric keys, which is why CNSA 2.0 requires AES-256 rather than AES-128.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Harvest now, decrypt later", "description": "Harvest now, decrypt later is the attack of recording encrypted data today in order to decrypt it once a cryptographically relevant quantum computer exists. It makes post-quantum key establishment urgent for data that must stay confidential for years.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "ML-KEM (FIPS 203)", "description": "ML-KEM is the NIST-standard lattice-based key-encapsulation mechanism, formerly CRYSTALS-Kyber. ML-KEM-768 has a 1,184-byte public key, a 1,088-byte ciphertext and a 32-byte shared secret; ML-KEM-1024 is the CNSA 2.0 parameter set.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "ML-DSA (FIPS 204)", "description": "ML-DSA is the NIST-standard lattice-based digital signature algorithm, formerly CRYSTALS-Dilithium. ML-DSA-65 has a 1,952-byte public key and a 3,309-byte signature; ML-DSA-87 is the CNSA 2.0 parameter set.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "SLH-DSA (FIPS 205)", "description": "SLH-DSA is the NIST-standard stateless hash-based signature algorithm, formerly SPHINCS+. Its security rests only on hash functions; signatures are large (7,856 bytes for SLH-DSA-SHA2-128s).", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "FN-DSA", "description": "FN-DSA is the forthcoming NIST signature standard (FIPS 206) based on Falcon, with smaller signatures than ML-DSA and a more delicate implementation.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "HQC", "description": "HQC is a code-based key-encapsulation mechanism that NIST selected in 2025 for standardisation as a backup to ML-KEM, built on different mathematics.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Key-encapsulation mechanism (KEM)", "description": "A key-encapsulation mechanism is a public-key scheme in which a sender uses the recipient's public key to produce a ciphertext and a shared secret, which only the recipient's private key can recover. It replaces Diffie–Hellman-style key agreement in post-quantum protocols.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Hybrid key exchange", "description": "Hybrid key exchange combines a post-quantum KEM and a classical key agreement, such as ML-KEM-768 with X25519, and derives one secret from both, so the result stays secure if either component is broken.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "X25519MLKEM768", "description": "X25519MLKEM768 is the hybrid key-exchange group used in TLS 1.3 that combines X25519 with ML-KEM-768. It is the most widely deployed post-quantum mechanism on the web.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Composite signature", "description": "A composite signature pairs a post-quantum and a classical signature (for example ML-DSA-65 with Ed25519) under one key and one verification decision; both must verify.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Crypto agility", "description": "Crypto agility is the ability to change cryptographic algorithms through configuration or a small, contained code change, without redesigning a system. It makes this and future migrations cheaper.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Cryptography Bill of Materials (CBOM)", "description": "A Cryptography Bill of Materials is a machine-readable inventory of the algorithms, keys, protocols and certificates a system uses, typically in CycloneDX format. It is the basis for migration planning and audit.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "CycloneDX", "description": "CycloneDX is an OWASP standard for bills of materials. Version 1.6 includes cryptographic assets, which is how CBOMs are written.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "SARIF", "description": "SARIF (Static Analysis Results Interchange Format, OASIS 2.1.0) is a JSON format for static-analysis findings that code-scanning tools such as GitHub code scanning can display.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "CNSA 2.0", "description": "CNSA 2.0 is the NSA's Commercial National Security Algorithm Suite 2.0: ML-KEM-1024, ML-DSA-87, LMS and XMSS, AES-256 and SHA-384/512, with transition deadlines from 2025 to 2033 depending on the system type.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "NIST IR 8547", "description": "NIST IR 8547 is NIST's draft guidance on transitioning to post-quantum cryptography. It deprecates 112-bit quantum-vulnerable algorithms after 2030 and disallows quantum-vulnerable public-key algorithms after 2035.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "FIPS 140-3 and CMVP", "description": "FIPS 140-3 is the US standard for cryptographic modules, and the Cryptographic Module Validation Program (CMVP) is how accredited laboratories validate modules against it. No PQBlocks package is CMVP validated.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "ACVP", "description": "ACVP (Automated Cryptographic Validation Protocol) is NIST's protocol and test-vector format for checking that an algorithm implementation produces the right results.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Known-answer test (KAT)", "description": "A known-answer test runs an implementation on fixed inputs and compares its outputs with published expected values, catching implementation errors that random testing can miss.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Wycheproof", "description": "Wycheproof is a collection of test vectors for known attacks and edge cases in cryptographic libraries, such as malformed inputs and invalid curve points.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "liboqs", "description": "liboqs is the Open Quantum Safe project's C library of post-quantum algorithms. Several PQBlocks packages use it for ML-KEM, ML-DSA and SLH-DSA rather than re-implementing them.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "QUBO", "description": "A QUBO (quadratic unconstrained binary optimisation) problem minimises a quadratic function of binary variables. Many scheduling, routing and selection problems can be written this way.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Ising model", "description": "An Ising model assigns spins of +1 or −1 to variables and minimises an energy with pairwise couplings and local fields. It is equivalent to a QUBO up to a change of variables.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Simulated bifurcation", "description": "Simulated bifurcation is a quantum-inspired classical heuristic (Goto et al., 2019 and 2021) that evolves continuous oscillators which bifurcate into ±1 states to find low-energy Ising solutions.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}, {"@type": "DefinedTerm", "name": "Quantum-inspired optimisation", "description": "Quantum-inspired optimisation is classical algorithms modelled on quantum dynamics, such as annealing or bifurcation, run on ordinary hardware. It involves no quantum computer and has no security role.", "inDefinedTermSet": "https://pqblocks.github.io/glossary/"}]}
---
<!-- GENERATED by scripts/gen_docs.py from data/catalog.json - do not edit by hand -->


# Glossary

<p class="pqb-lead">The terms used across PQBlocks, each in a sentence or two.</p>

### ACVP

ACVP (Automated Cryptographic Validation Protocol) is NIST's protocol and test-vector format for checking that an algorithm implementation produces the right results.

### CNSA 2.0

CNSA 2.0 is the NSA's Commercial National Security Algorithm Suite 2.0: ML-KEM-1024, ML-DSA-87, LMS and XMSS, AES-256 and SHA-384/512, with transition deadlines from 2025 to 2033 depending on the system type.

### Composite signature

A composite signature pairs a post-quantum and a classical signature (for example ML-DSA-65 with Ed25519) under one key and one verification decision; both must verify.

### Crypto agility

Crypto agility is the ability to change cryptographic algorithms through configuration or a small, contained code change, without redesigning a system. It makes this and future migrations cheaper.

### Cryptographically relevant quantum computer (CRQC)

A cryptographically relevant quantum computer is a quantum computer large and reliable enough to run Shor's algorithm against real RSA and elliptic-curve keys. None is known to exist; migration deadlines are set so systems move before one does.

### Cryptography Bill of Materials (CBOM)

A Cryptography Bill of Materials is a machine-readable inventory of the algorithms, keys, protocols and certificates a system uses, typically in CycloneDX format. It is the basis for migration planning and audit.

### CycloneDX

CycloneDX is an OWASP standard for bills of materials. Version 1.6 includes cryptographic assets, which is how CBOMs are written.

### FIPS 140-3 and CMVP

FIPS 140-3 is the US standard for cryptographic modules, and the Cryptographic Module Validation Program (CMVP) is how accredited laboratories validate modules against it. No PQBlocks package is CMVP validated.

### FN-DSA

FN-DSA is the forthcoming NIST signature standard (FIPS 206) based on Falcon, with smaller signatures than ML-DSA and a more delicate implementation.

### Grover's algorithm

Grover's algorithm is a quantum search algorithm with a quadratic speed-up. It roughly halves the effective strength of symmetric keys, which is why CNSA 2.0 requires AES-256 rather than AES-128.

### Harvest now, decrypt later

Harvest now, decrypt later is the attack of recording encrypted data today in order to decrypt it once a cryptographically relevant quantum computer exists. It makes post-quantum key establishment urgent for data that must stay confidential for years.

### HQC

HQC is a code-based key-encapsulation mechanism that NIST selected in 2025 for standardisation as a backup to ML-KEM, built on different mathematics.

### Hybrid key exchange

Hybrid key exchange combines a post-quantum KEM and a classical key agreement, such as ML-KEM-768 with X25519, and derives one secret from both, so the result stays secure if either component is broken.

### Ising model

An Ising model assigns spins of +1 or −1 to variables and minimises an energy with pairwise couplings and local fields. It is equivalent to a QUBO up to a change of variables.

### Key-encapsulation mechanism (KEM)

A key-encapsulation mechanism is a public-key scheme in which a sender uses the recipient's public key to produce a ciphertext and a shared secret, which only the recipient's private key can recover. It replaces Diffie–Hellman-style key agreement in post-quantum protocols.

### Known-answer test (KAT)

A known-answer test runs an implementation on fixed inputs and compares its outputs with published expected values, catching implementation errors that random testing can miss.

### liboqs

liboqs is the Open Quantum Safe project's C library of post-quantum algorithms. Several PQBlocks packages use it for ML-KEM, ML-DSA and SLH-DSA rather than re-implementing them.

### ML-DSA (FIPS 204)

ML-DSA is the NIST-standard lattice-based digital signature algorithm, formerly CRYSTALS-Dilithium. ML-DSA-65 has a 1,952-byte public key and a 3,309-byte signature; ML-DSA-87 is the CNSA 2.0 parameter set.

### ML-KEM (FIPS 203)

ML-KEM is the NIST-standard lattice-based key-encapsulation mechanism, formerly CRYSTALS-Kyber. ML-KEM-768 has a 1,184-byte public key, a 1,088-byte ciphertext and a 32-byte shared secret; ML-KEM-1024 is the CNSA 2.0 parameter set.

### NIST IR 8547

NIST IR 8547 is NIST's draft guidance on transitioning to post-quantum cryptography. It deprecates 112-bit quantum-vulnerable algorithms after 2030 and disallows quantum-vulnerable public-key algorithms after 2035.

### Post-quantum cryptography (PQC)

Post-quantum cryptography is public-key cryptography designed to resist attacks by large quantum computers while running on ordinary computers. The first NIST standards are ML-KEM, ML-DSA and SLH-DSA.

### Quantum-inspired optimisation

Quantum-inspired optimisation is classical algorithms modelled on quantum dynamics, such as annealing or bifurcation, run on ordinary hardware. It involves no quantum computer and has no security role.

### QUBO

A QUBO (quadratic unconstrained binary optimisation) problem minimises a quadratic function of binary variables. Many scheduling, routing and selection problems can be written this way.

### SARIF

SARIF (Static Analysis Results Interchange Format, OASIS 2.1.0) is a JSON format for static-analysis findings that code-scanning tools such as GitHub code scanning can display.

### Shor's algorithm

Shor's algorithm is a quantum algorithm that factors integers and computes discrete logarithms in polynomial time, which breaks RSA, Diffie–Hellman, DSA and elliptic-curve cryptography.

### Simulated bifurcation

Simulated bifurcation is a quantum-inspired classical heuristic (Goto et al., 2019 and 2021) that evolves continuous oscillators which bifurcate into ±1 states to find low-energy Ising solutions.

### SLH-DSA (FIPS 205)

SLH-DSA is the NIST-standard stateless hash-based signature algorithm, formerly SPHINCS+. Its security rests only on hash functions; signatures are large (7,856 bytes for SLH-DSA-SHA2-128s).

### Wycheproof

Wycheproof is a collection of test vectors for known attacks and edge cases in cryptographic libraries, such as malformed inputs and invalid curve points.

### X25519MLKEM768

X25519MLKEM768 is the hybrid key-exchange group used in TLS 1.3 that combines X25519 with ML-KEM-768. It is the most widely deployed post-quantum mechanism on the web.
