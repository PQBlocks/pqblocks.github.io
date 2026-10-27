---
title: How to encrypt files with a post-quantum key in Python
description: Encrypt files to an ML-KEM-768 + X25519 hybrid public key with passphrase-sealed key files using pqblocks-files. Complete, tested code.
---

# How to encrypt files with a post-quantum key in Python

<p class="pqb-lead">Create a hybrid ML-KEM-768 + X25519 key pair, store it on disk with the private key sealed under a passphrase, encrypt a file to the public key and decrypt it again. Uses <code>pqblocks-files</code>.</p>

## The problem

Archives, backups and exported reports are exactly what *harvest now, decrypt later* targets: they are stored for years. Files encrypted to an RSA or X25519 public key today can be opened once a quantum computer exists. `pqblocks-files` wraps each file key with both ML-KEM-768 and X25519 and seals the content in authenticated 64 KiB ChaCha20-Poly1305 chunks.

## Install

```bash
pip install git+https://github.com/PQBlocks/hybrid-file-encryption
```

ML-KEM comes from [liboqs](https://openquantumsafe.org/liboqs/); see the [package page](../packages/files.md#install).

## Complete working code

```python title="encrypt_files.py"
--8<-- "recipes/code/encrypt_files.py"
```

Output:

```text
encrypted 31000 bytes and decrypted them back: OK
```

## How it works

1. `keygen()` creates one ML-KEM-768 and one X25519 key pair.
2. `save_private_key` seals the private half with scrypt and a random salt and writes it with mode `0600`.
3. `encrypt` draws a fresh random file key, wraps it for each recipient with **both** algorithms, and encrypts the content in authenticated chunks. Several recipients can be listed.
4. `decrypt` refuses files that were wrapped with X25519 only, unless you explicitly pass `require_pq=False`. A downgraded file cannot be slipped past you.

## Things to know

- Pre-1.0 and not independently audited; not FIPS or CMVP validated. Read the [security notes](https://github.com/PQBlocks/hybrid-file-encryption/blob/main/SECURITY_NOTES.md).
- Never hard-code the passphrase. Prompt for it or read it from a secret store.
- A command-line interface ships with the package; see its [README](https://github.com/PQBlocks/hybrid-file-encryption#readme).

## Related

- [`pqblocks-files`](../packages/files.md) · [Hybrid X25519 + ML-KEM](hybrid-kem.md)
