import pathlib, tempfile
from pqblocks_lint import cli

src = pathlib.Path(tempfile.mkdtemp(), "keys.py")
src.write_text("from cryptography.hazmat.primitives.asymmetric import rsa\n"
               "def make_key():\n"
               "    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)\n"
               "    return key\n")
code = cli.main(["--target", str(src), "--format", "cbom", "--output", str(src.with_suffix(".cbom.json")), "--seed", "0"])
print(code)   # 1: quantum-vulnerable cryptography found (RSA-2048)
