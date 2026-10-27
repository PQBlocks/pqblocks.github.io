import ctypes, os
import pqblocks_core

# Locate the native hybrid KEM library
lib_path = os.path.join(os.path.dirname(pqblocks_core.__file__), "lib", "libpqblocks_kem.so")
lib = ctypes.CDLL(lib_path)
lib.PQBLOCKS_KEM_X25519_MLKEM768_new.restype = ctypes.c_void_p

# Initialize hybrid KEM handle (ML-KEM-768 + X25519)
kem = lib.PQBLOCKS_KEM_X25519_MLKEM768_new()
assert kem is not None
print("PQBlocks hybrid core initialized successfully.")
