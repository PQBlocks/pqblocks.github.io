---
title: How to implement post-quantum hybrid authentication in Express
description: Protect Express routes using dual-scheme hybrid tokens combining classical Ed25519 and NIST FIPS 204 ML-DSA-65 signatures. Complete, tested code and output.
---

# How to implement post-quantum hybrid authentication in Express

<p class="pqb-lead">Add dual-signature hybrid authentication middleware to an Express.js server, combining classical Ed25519 and NIST FIPS 204 ML-DSA-65 to protect APIs against quantum cryptanalysis.</p>

## The problem

Single-algorithm tokens leave web services exposed to sudden algorithmic breaks. If your service uses only classical RSA or ECDSA, an attacker with a cryptographically relevant quantum computer can forge tokens. If your service switches prematurely to a post-quantum algorithm with unproven implementation robustness, an unexpected classical vulnerability could compromise security. A hybrid authentication scheme requires every bearer token to verify under **both** a classical and a post-quantum signature algorithm simultaneously.

## Install

=== "npm"

    ```bash
    npm i express @noble/post-quantum
    ```

=== "pnpm"

    ```bash
    pnpm add express @noble/post-quantum
    ```

=== "bun"

    ```bash
    bun add express @noble/post-quantum
    ```

=== "yarn"

    ```bash
    yarn add express @noble/post-quantum
    ```

## Complete working code

=== "JavaScript (Node.js / ESM)"

    ```javascript title="express_hybrid_auth.mjs"
    --8<-- "recipes/code/express_hybrid_auth.mjs"
    ```

=== "TypeScript"

    ```typescript title="express_hybrid_auth.ts"
    import express, { type Request, type Response, type NextFunction } from 'express';
    import crypto from 'node:crypto';
    import { ml_dsa65 } from '@noble/post-quantum/ml-dsa.js';

    export interface HybridTokenPayload {
      sub: string;
      iat: number;
    }

    export interface HybridTokenContainer {
      payload: string;      // base64url JSON
      classicalSig: string; // base64url Ed25519 signature
      pqcSig: string;       // base64url ML-DSA-65 signature
    }

    export function hybridAuthMiddleware(
      classicalPubKey: crypto.KeyObject,
      pqcPubKey: Uint8Array
    ) {
      return (req: Request, res: Response, next: NextFunction): void => {
        const header = req.headers['authorization'];
        if (!header || !header.startsWith('Hybrid ')) {
          res.status(401).json({ error: 'Missing or malformed Authorization header' });
          return;
        }

        try {
          const raw = Buffer.from(header.slice(7), 'base64url').toString('utf8');
          const token: HybridTokenContainer = JSON.parse(raw);
          const payloadBytes = Buffer.from(token.payload, 'base64url');

          // 1. Verify Classical (Ed25519) signature
          const isClassicalValid = crypto.verify(
            null,
            payloadBytes,
            classicalPubKey,
            Buffer.from(token.classicalSig, 'base64url')
          );
          if (!isClassicalValid) {
            res.status(401).json({ error: 'Invalid classical signature' });
            return;
          }

          // 2. Verify Post-Quantum (ML-DSA-65) signature
          const isPqcValid = ml_dsa65.verify(
            Buffer.from(token.pqcSig, 'base64url'),
            payloadBytes,
            pqcPubKey
          );
          if (!isPqcValid) {
            res.status(401).json({ error: 'Invalid post-quantum signature' });
            return;
          }

          (req as any).user = JSON.parse(payloadBytes.toString('utf8')) as HybridTokenPayload;
          next();
        } catch {
          res.status(401).json({ error: 'Malformed hybrid token structure' });
        }
      };
    }
    ```

Output:

```text
valid hybrid auth: HTTP 200 authenticated: true
tampered pqc credential: HTTP 401 Unauthorized
tampered classical credential: HTTP 401 Unauthorized
server closed
```

## How it works

1. **Composite Token Issuance.** The authentication server signs the token payload twice: first with classical Ed25519 (64-byte signature), and second with ML-DSA-65 (3,309-byte signature).
2. **Strict Dual Verification.** The Express middleware evaluates both signatures sequentially. If either signature fails verification or is omitted, the request is immediately rejected with HTTP 401 Unauthorized.
3. **Defense in Depth.** Security holds so long as *either* Ed25519 remains resistant to classical attacks *or* ML-DSA-65 remains resistant to quantum attacks.

## Things to know

- **Header Sizes:** ML-DSA-65 signatures are 3,309 bytes. Ensure your reverse proxy (e.g. Nginx, Envoy, Cloudflare) is configured to permit `client_header_buffer_size 16k;` or `max_header_size: 16384`.
- **Pure JavaScript:** `@noble/post-quantum` has zero native compilation dependencies, making it safe for deployment across containerized Node.js, Alpine Linux, or serverless runtimes.

## Related

- [How to verify post-quantum certificate chains in Node.js and the browser](browser-verification.md)
- [How to add post-quantum tokens to FastAPI](fastapi-pqc.md)
- [How to sign JWTs with ML-DSA in Python](jwt-ml-dsa.md)
