#!/usr/bin/env node
/**
 * Express Recipe: Post-Quantum + Classical Hybrid Authentication Middleware.
 * Combines classical Ed25519 with NIST FIPS 204 ML-DSA-65 signatures.
 */
import express from 'express';
import crypto from 'node:crypto';
import { ml_dsa65 } from '@noble/post-quantum/ml-dsa.js';

// 1. Generate Classical (Ed25519) and Post-Quantum (ML-DSA-65) server keys
const classicalKeyPair = crypto.generateKeyPairSync('ed25519');
const pqcSeed = new Uint8Array(32).fill(42); // deterministic seed for test reproducibility
const pqcKeys = ml_dsa65.keygen(pqcSeed);

// Helper: Issue a dual/hybrid bearer token
function issueHybridToken(subject) {
  const payload = JSON.stringify({ sub: subject, iat: Math.floor(Date.now() / 1000) });
  const payloadBytes = Buffer.from(payload, 'utf8');

  // Classical signature (Ed25519)
  const classicalSig = crypto.sign(null, payloadBytes, classicalKeyPair.privateKey);

  // Post-quantum signature (ML-DSA-65)
  const pqcSig = ml_dsa65.sign(payloadBytes, pqcKeys.secretKey);

  return {
    payload: payloadBytes.toString('base64url'),
    classicalSig: classicalSig.toString('base64url'),
    pqcSig: Buffer.from(pqcSig).toString('base64url'),
  };
}

// 2. Hybrid Authentication Express Middleware
function hybridAuthMiddleware(req, res, next) {
  const authHeader = req.headers['authorization'];
  if (!authHeader || !authHeader.startsWith('Hybrid ')) {
    return res.status(401).json({ error: 'Missing or malformed Authorization header' });
  }

  try {
    const raw = Buffer.from(authHeader.slice(7), 'base64url').toString('utf8');
    const { payload, classicalSig, pqcSig } = JSON.parse(raw);
    const payloadBytes = Buffer.from(payload, 'base64url');

    // Verify Classical (Ed25519) signature
    const classicalValid = crypto.verify(
      null,
      payloadBytes,
      classicalKeyPair.publicKey,
      Buffer.from(classicalSig, 'base64url')
    );
    if (!classicalValid) {
      return res.status(401).json({ error: 'Invalid classical signature' });
    }

    // Verify Post-Quantum (ML-DSA-65) signature
    const pqcValid = ml_dsa65.verify(
      Buffer.from(pqcSig, 'base64url'),
      payloadBytes,
      pqcKeys.publicKey
    );
    if (!pqcValid) {
      return res.status(401).json({ error: 'Invalid post-quantum signature' });
    }

    req.user = JSON.parse(payloadBytes.toString('utf8'));
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Malformed hybrid token' });
  }
}

// 3. Setup Express app
const app = express();
app.use(express.json());

app.get('/api/protected', hybridAuthMiddleware, (req, res) => {
  res.json({ authenticated: true, user: req.user.sub, mode: 'ML-DSA-65+Ed25519' });
});

// 4. Run test queries against listening server
const server = app.listen(0, async () => {
  const port = server.address().port;
  const baseUrl = `http://127.0.0.1:${port}/api/protected`;

  // Test A: Valid Hybrid Token
  const validToken = issueHybridToken('alice@example.com');
  const validHeader = 'Hybrid ' + Buffer.from(JSON.stringify(validToken)).toString('base64url');
  const resA = await fetch(baseUrl, { headers: { Authorization: validHeader } });
  const dataA = await resA.json();
  console.log(`valid hybrid auth: HTTP ${resA.status} authenticated: ${dataA.authenticated}`);

  // Test B: Tampered PQC Signature
  const badPqcToken = { ...validToken, pqcSig: 'AAAA' + validToken.pqcSig.slice(4) };
  const badPqcHeader = 'Hybrid ' + Buffer.from(JSON.stringify(badPqcToken)).toString('base64url');
  const resB = await fetch(baseUrl, { headers: { Authorization: badPqcHeader } });
  console.log(`tampered pqc credential: HTTP ${resB.status} Unauthorized`);

  // Test C: Tampered Classical Signature
  const badClassToken = { ...validToken, classicalSig: 'BBBB' + validToken.classicalSig.slice(4) };
  const badClassHeader = 'Hybrid ' + Buffer.from(JSON.stringify(badClassToken)).toString('base64url');
  const resC = await fetch(baseUrl, { headers: { Authorization: badClassHeader } });
  console.log(`tampered classical credential: HTTP ${resC.status} Unauthorized`);

  server.close(() => {
    console.log('server closed');
  });
});
