import sys
import os
from itertools import cycle
import gzip


def ror(n, rotations, width):
    return (2**width - 1) & (n >> rotations | n << (width - rotations))


def rol(n, rotations, width):
    return (2**width - 1) & (n << rotations | n >> (width - rotations))


with open("3/withkey/juliakey.txt", "r") as julia_key_file, open(
    "3/withkey/juliaplaintext.txt.gz.enc", "rb"
) as julia_cipher_file:
    julia_key_content = julia_key_file.read()
    key_shift = int(julia_key_content.split()[4])
    key_xor = julia_key_content.split()[-1]
    print("key shift", key_shift)
    print("key xor", key_xor)

    julia_cipher_content = julia_cipher_file.read()
    result = bytes()
    for c_byte, k_byte in zip(julia_cipher_content, cycle(key_xor)):
        tmp = c_byte ^ ord(k_byte)
        # kinda misleading, question mentions that encryption rotates bits but didn't mention which direction
        # imagine spending 3 hours thinking it's gzip when it turns out you rotate RIGHT
        result += ror(c_byte ^ ord(k_byte), 1, 8).to_bytes(1, "big")
        
	# gzip - write as bytes, read with decompression
    with open("test.gz", "wb") as f:
        f.write(result)
    with gzip.open("test.gz", "r") as gf:
        print(gf.read().decode())
    os.remove("test.gz")
