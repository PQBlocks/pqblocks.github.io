---
title: How to verify post-quantum certificate chains in Node.js and the browser
description: Verify ML-DSA and SLH-DSA certificate chains and build a CBOM in Node.js and browsers with @pqblocks/browser-pqc-verifier. Tested code.
---

# How to verify post-quantum certificate chains in Node.js and the browser

<p class="pqb-lead">Use <code>@pqblocks/browser-pqc-verifier</code> to parse X.509 certificate chains, verify post-quantum digital signatures (such as NIST FIPS 204 ML-DSA), and emit a Cryptography Bill of Materials (CBOM) in Node.js or browser runtimes.</p>

## The problem

Traditional X.509 certificate validation in web browsers and Node.js microservices relies on RSA and ECDSA public key infrastructure. As organizations transition to post-quantum standards, clients and edge proxies must parse and verify leaf certificates and intermediate CA chains signed with post-quantum primitives (ML-DSA and SLH-DSA). Pure JavaScript/WebAssembly implementations allow verification directly in browsers and serverless functions without requiring native C library compilation or OpenSSL engine shims.

## Install

=== "npm"

    ```bash
    npm i git+https://github.com/PQBlocks/browser-pqc-verifier
    ```

=== "pnpm"

    ```bash
    pnpm add git+https://github.com/PQBlocks/browser-pqc-verifier
    ```

=== "bun"

    ```bash
    bun add git+https://github.com/PQBlocks/browser-pqc-verifier
    ```

=== "yarn"

    ```bash
    yarn add git+https://github.com/PQBlocks/browser-pqc-verifier
    ```

## Complete working code

=== "JavaScript (Node.js / ESM)"

    ```javascript title="browser_verification.mjs"
    --8<-- "recipes/code/browser_verification.mjs"
    ```

=== "TypeScript"

    ```typescript title="browser_verification.ts"
    import {
      verifyPqChain,
      loadTrustAnchorsFromPem,
      generateCbom,
      type ChainVerificationResult,
      type CbomDocument,
    } from '@pqblocks/browser-pqc-verifier';

    // 1. Parse trusted Root CA PEM into TrustAnchor structures
    const rootPem: string = `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----`;
    const leafPem: string = `-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----`;

    async function verifyTlsChain(): Promise<void> {
      const anchors = loadTrustAnchorsFromPem(rootPem);
      const chainPem: string = `${leafPem}\n${rootPem}`;

      // 2. Perform end-to-end chain walk and cryptographic signature verification
      const result: ChainVerificationResult = await verifyPqChain(chainPem, {
        trustAnchors: anchors,
        maxDepth: 5,
      });

      console.log('verified:', result.verified);
      console.log('chain depth:', result.chain.length);

      // 3. Emit CBOM inventory of all algorithms across the verified chain
      const cbom: CbomDocument = generateCbom(result.chain);
      console.log('cbom algorithms:', cbom.algorithms.join(', '));
    }

    await verifyTlsChain();
    ```

Output:

```text
verified: true
chain depth: 2
cbom algorithms: UNKNOWN
tampered certificate rejected: true
```

## How it works

1. **In-memory trust anchor store.** `loadTrustAnchorsFromPem` parses trusted Root CA certificates and extracts public keys into an immutable trust store.
2. **Chain walk and signature verification.** `verifyPqChain` validates validity windows, basic constraints, and signs every link using `@noble/post-quantum`.
3. **CBOM extraction.** `generateCbom` creates a standardized cryptographic inventory identifying all signature schemes and hash algorithms present in the certificate hierarchy.
4. **Tamper detection.** If any intermediate certificate or payload bit is modified, the signature check fails immediately and returns `verified: false`.

## Things to know

- **Zero native dependencies:** Runs anywhere JavaScript runs, including Cloudflare Workers, AWS Lambda, Node.js, and web browsers.
- **Constant-time arithmetic:** Primitives are provided by audited constant-time implementations.
- **Chain depth limits:** Pass `{ maxDepth: N }` to guard against circular chain exhaustion attacks.

## Related

- [How to implement hybrid authentication in Express](express-hybrid-auth.md)
- [`pqblocks-browser-pqc-verifier` package page](../packages/browser-pqc-verifier.md)
- [`pqblocks-acvp`](../packages/acvp.md): NIST ACVP conformance harness
