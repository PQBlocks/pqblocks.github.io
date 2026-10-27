"""Encrypt a file to a post-quantum hybrid public key and decrypt it (pqblocks-files)."""
import os
import tempfile

from pqblocks_files.encrypt import decrypt, encrypt
from pqblocks_files.keys import keygen, load_private_key, load_public_key, save_private_key, save_public_key
from pqblocks_files.pqtypes import KeyPair

with tempfile.TemporaryDirectory() as d:
    # 1. Create a key pair and store it; the private key is sealed under a passphrase (scrypt, mode 0600).
    passphrase = os.urandom(16).hex().encode()        # demo only: prompt for it or use a secret store
    kp = keygen()                                     # ML-KEM-768 + X25519
    save_public_key(kp, os.path.join(d, "alice.pub"))
    save_private_key(kp, os.path.join(d, "alice.key"), passphrase)

    # 2. Anyone with the public key can encrypt.
    report = b"Q3 board report - confidential\n" * 1000
    recipient = load_public_key(os.path.join(d, "alice.pub"))
    with open(os.path.join(d, "report.pfsh"), "wb") as fh:
        fh.write(encrypt(report, [recipient]))

    # 3. Only the private key holder can decrypt.
    me = KeyPair(public=recipient, private=load_private_key(os.path.join(d, "alice.key"), passphrase))
    with open(os.path.join(d, "report.pfsh"), "rb") as fh:
        assert decrypt(fh.read(), me) == report
    print("encrypted", len(report), "bytes and decrypted them back: OK")
