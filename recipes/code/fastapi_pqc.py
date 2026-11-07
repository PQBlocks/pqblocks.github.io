"""FastAPI service that issues and checks hybrid ML-DSA-65 + Ed25519 signed tokens (pqblocks-jose)."""
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pqblocks_jose import Policy, decode_jws, encode_jws, generate_keypair

POLICY = Policy(
    version=1,
    kem="X25519+MLKEM768",
    sig="MLDSA65+Ed25519",
    kdf="HKDF-SHA256",
    max_token_bytes=8192,
    kdf_info="JOSE_PostQuantum_Traditional_Hybrid X25519MLKEM768",
    sig_alg_std="ML-DSA-65-Ed25519",
)
# Demo only: a real service loads its signing key from a secret store at start-up.
SIGNING_KEYS = generate_keypair("ML-DSA-65-Ed25519")

app = FastAPI(title="Post-quantum signed tokens")
bearer = HTTPBearer()


@app.post("/token")
def issue_token(user: str) -> dict:
    claims = {"sub": user, "aud": "api.example.com"}
    signed = encode_jws(claims, POLICY, private_key=SIGNING_KEYS.private_key)
    return {"access_token": signed.compact_serialization, "token_type": "Bearer"}


def verified_token(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> str:
    try:
        result = decode_jws(token=creds.credentials, policy=POLICY, public_key=SIGNING_KEYS.public_key)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")
    if not result.signature_verified:
        raise HTTPException(status_code=401, detail="invalid token")
    return creds.credentials


@app.get("/me")
def me(token: str = Depends(verified_token)) -> dict:
    return {"ok": True, "token_bytes": len(token)}


if __name__ == "__main__":
    # Self-check without a server: issue a token, use it, then tamper with it.
    from fastapi.testclient import TestClient

    client = TestClient(app)
    tok = client.post("/token", params={"user": "alice"}).json()["access_token"]
    assert client.get("/me", headers={"Authorization": "Bearer " + tok}).status_code == 200
    tampered = tok[:-8] + ("A" * 8 if not tok.endswith("A" * 8) else "B" * 8)
    assert client.get("/me", headers={"Authorization": "Bearer " + tampered}).status_code == 401
    print("issued, accepted, tampered token rejected: OK")
