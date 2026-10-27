from pqblocks_files.encrypt import encrypt, decrypt
from pqblocks_files.keys import keygen

keypair = keygen()                                    # ML-KEM-768 + X25519
blob = encrypt(b"quarterly numbers", [keypair.public])  # fresh random file key every call
assert decrypt(blob, keypair) == b"quarterly numbers"   # refuses classical-only files by default
