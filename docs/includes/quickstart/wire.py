from pqblocks_wire import (generate_mlkem_keypair, encapsulate_mlkem, decapsulate_mlkem,
                           encode_wire_format, decode_wire_format)

pk, sk = generate_mlkem_keypair("ML-KEM-768")
ct, ss_sender = encapsulate_mlkem(pk, "ML-KEM-768")
frame = encode_wire_format(mlkem_ciphertext=ct, payload=b"hello")      # 1109 bytes
received = decode_wire_format(frame)
ss_receiver = decapsulate_mlkem(sk, received.mlkem_ciphertext, "ML-KEM-768")
print(ss_sender == ss_receiver, received.payload)                    # True b'hello'
