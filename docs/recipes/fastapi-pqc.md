# How to Add Post-Quantum Encryption to FastAPI

Learn how to secure FastAPI API endpoints using post-quantum hybrid JSON Web Encryption (JWE) tokens with ML-KEM-768 and X25519.

## The Problem

Standard JWTs using HMAC or classical RSA/ECDSA can be recorded today and decrypted by an adversary with access to a future cryptographically relevant quantum computer. Sensitive session tokens and authorization payloads must transition to quantum-safe hybrid encryption.

## Installation

```bash
pip install fastapi uvicorn pqblocks-jwe
```

## Complete Working Code

```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pqblocks_jwe import encrypt_jwe, decrypt_jwe, generate_hybrid_keypair

app = FastAPI(title="Quantum-Safe Authentication API")
security = HTTPBearer()

# Generate or load the server's post-quantum hybrid keypair
# (In production, load the private key from secure environment storage)
SERVER_PRIVATE_KEY, SERVER_PUBLIC_KEY = generate_hybrid_keypair()

@app.post("/auth/login")
def login(username: str):
    """Issues a post-quantum encrypted JWE token upon login."""
    # Build session claims
    claims = f'{{"user":"{username}","role":"admin"}}'.encode("utf-8")
    
    # Encrypt into compact 5-part JWE token using server public key
    token = encrypt_jwe(claims, SERVER_PUBLIC_KEY)
    return {"access_token": token, "token_type": "Bearer"}

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Validates and decrypts the JWE token."""
    token = credentials.credentials
    try:
        decrypted_payload = decrypt_jwe(token, SERVER_PRIVATE_KEY)
        return decrypted_payload.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or unreadable post-quantum token")

@app.get("/api/v1/secure-data")
def get_secure_data(user_claims: str = Depends(verify_token)):
    """Protected endpoint only accessible with a valid post-quantum JWE token."""
    return {"message": "Access granted to quantum-safe vault", "claims": user_claims}
```

## How It Works

1. **Hybrid Key Encapsulation:** When generating the token, `encrypt_jwe` encapsulates a symmetric content encryption key (AES-256-GCM) using both **ML-KEM-768** (FIPS 203) and **X25519** (RFC 7748).
2. **Compact RFC 7516 Token:** The token conforms to the 5-part base64url JWE standard: `header.encrypted_key.iv.ciphertext.tag`.
3. **Defense-in-Depth:** An attacker must break *both* lattice cryptography and classical elliptic curves to recover the decrypted claims.

## Security Notes

- The server's private key must remain in memory or hardware HSM and never be committed to source repositories.
- Use TLS 1.3 in transport to prevent active man-in-the-middle manipulation.
