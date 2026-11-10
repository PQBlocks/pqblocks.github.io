---
title: "Software Development Kits (SDKs)"
description: "End-to-end post-quantum software development kits providing native C shared libraries, multi-language bindings, and policy enforcement."
schema: {"@context": "https://schema.org", "@type": "CollectionPage", "name": "PQBlocks: Software Development Kits (SDKs)", "description": "End-to-end post-quantum software development kits providing native C shared libraries, multi-language bindings, and policy enforcement.", "url": "https://pqblocks.github.io/packages/sdks/", "hasPart": [{"@type": "SoftwareSourceCode", "name": "pqblocks-core", "codeRepository": "https://github.com/PQBlocks/hybrid-sdk"}]}
---

# :material-cube-scan: Software Development Kits (SDKs)

<p class="pqb-lead">End-to-end software development kits bundling native C acceleration, multi-language interfaces, and policy-as-code governance for building production-grade post-quantum applications.</p>

While individual PQBlocks libraries provide targeted point solutions (such as ACVP test runners or CBOM scanners), **PQBlocks SDKs** provide full-stack developer toolkits designed to serve as the foundational cryptographic layer for applications, microservices, and enterprise infrastructure.

---

## Why use an SDK instead of individual dependencies?

| Capability | PQBlocks Core SDK (`hybrid-sdk`) | Granular Dependencies |
|---|---|---|
| **Architectural Scope** | Complete hybrid KEM & composite signature engine | Single-purpose utility (e.g. OID lookup, token parser) |
| **Performance Acceleration** | Native C shared libraries (`libpqblocks_kem.so`, `libpqblocks_sig.so`) | Interpreted Python or Node.js execution |
| **Cryptographic Agility** | Built-in policy governance and CNSA 2.0 enforcement rules | Requires manual algorithm selection in caller code |
| **Integration Interfaces** | Dual-interface: high-level Python API + C/C++ CMake headers | Language-specific single distribution |
| **Hardware Hooks** | Extensible HSM and hardware-acceleration interfaces (`pqblocks_hsm.h`) | Software-only primitives |

---

## Available SDKs

<div class="grid cards" markdown>

-   :material-shield-key-outline:{ .lg .middle } __[`pqblocks-core` (hybrid-sdk)](core.md)__

    ---

    **Post-quantum hybrid cryptography core SDK** with C shared libraries and policy enforcement. Implements NIST FIPS 203 (ML-KEM-768 + X25519) and NIST FIPS 204 (ML-DSA-65 + Ed25519) with C-speed bindings.

    `pip install git+https://github.com/PQBlocks/hybrid-sdk`

</div>

---

## Quickstart: PQBlocks Core SDK

=== "Python"

    ```python
    import ctypes, os
    import pqblocks_core

    # Locate and bind to the native hybrid KEM library
    lib_path = os.path.join(os.path.dirname(pqblocks_core.__file__), "lib", "libpqblocks_kem.so")
    lib = ctypes.CDLL(lib_path)
    lib.PQBLOCKS_KEM_X25519_MLKEM768_new.restype = ctypes.c_void_p

    # Initialize hybrid KEM handle (ML-KEM-768 + X25519)
    kem = lib.PQBLOCKS_KEM_X25519_MLKEM768_new()
    assert kem is not None
    print("PQBlocks hybrid core initialized successfully.")
    ```

=== "C / Native CMake"

    ```bash
    # Clone the SDK repository
    git clone https://github.com/PQBlocks/hybrid-sdk.git
    cd hybrid-sdk

    # Build native shared libraries and headers
    cmake -B build -S .
    cmake --build build

    # Include in your C/C++ project:
    # #include "pqblocks_kem.h"
    # #include "pqblocks_sig.h"
    # #include "pqblocks_policy.h"
    ```

---

## Upcoming SDKs

The PQBlocks roadmap includes additional specialized SDKs currently in development:

* **Quantum-Safe Endpoint (QSE) SDK**: Lightweight client SDK providing automated TLS hybrid group negotiation, client certificate validation, and local policy enforcement for endpoints and microservices.
* **Post-Quantum CBOM CLI & SDK**: Programmatic SDK for CycloneDX 1.6 Cryptographic Bill of Materials generation, automated cryptographic asset inventory, and CI/CD policy gates.
