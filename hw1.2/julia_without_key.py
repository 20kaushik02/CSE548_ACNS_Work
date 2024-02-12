import sys
import os
from itertools import cycle
import gzip


def ror(n, rotations, width):
    return (2**width - 1) & (n >> rotations | n << (width - rotations))


with open("3/withoutkey/secretfile.txt.gz.enc", "rb") as julia_cipher_file:
    julia_cipher_content = julia_cipher_file.read()

# ASSUMPTION: gzip used with FNAME or FCOMMENT flag, and encodes the (known) filename after the initial 10-byte header
# if not, strat breaks down
filename = "secretfile.txt"
filename_bytes = filename.encode()
filename_bytes_enc = julia_cipher_content[10 : 10 + len(filename)]

# print("[+] Filename bytes:\t\t", filename_bytes.hex())
# print("[+] Filename bytes, encrypted:\t", filename_bytes_enc.hex())

key_length = 12
derived_rotation = 0
derived_key_bytes = bytearray(key_length)

# filename is 14 characters, key length is 12, so key wraps around, allowing us to check rotation amount
for byte in range(0, 256):
    possible_key_byte = bytes([byte])
    for possible_rotation in range(1, 8):
        if (
            ror(filename_bytes_enc[0] ^ possible_key_byte[0], possible_rotation, 8)
            == filename_bytes[0]
            and ror(
                filename_bytes_enc[key_length] ^ possible_key_byte[0],
                possible_rotation,
                8,
            )
            == filename_bytes[key_length]
        ):
            derived_rotation = possible_rotation
            break
    else:
        continue
    break
print("Rotation:", derived_rotation)

for idx in range(0, key_length):
    for byte in range(0, 256):
        possible_key_byte = bytes([byte])
        if (
            ror(filename_bytes_enc[idx] ^ possible_key_byte[0], derived_rotation, 8)
            == filename_bytes[idx]
        ):
            derived_key_bytes[(idx + 10) % key_length] = possible_key_byte[0]
            break
print("Key:", derived_key_bytes.hex())

result = bytes()
for c_byte, k_byte in zip(julia_cipher_content, cycle(derived_key_bytes)):
    result += ror(c_byte ^ k_byte, derived_rotation, 8).to_bytes(1, sys.byteorder)

# gzip - write as bytes, read with decompression
with open("test.gz", "wb") as f:
    f.write(result)
with gzip.open("test.gz", "r") as gf:
    print("answer starts here-----" + gf.read().decode() + "-----ends here")
os.remove("test.gz")
