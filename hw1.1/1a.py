import sys

with open("3/forstudents/a/ciphertext.bin", "rb") as cipher_file, open(
    "3/forstudents/a/key.bin", "rb"
) as key_file:
    cipher_content = cipher_file.read()
    key_content = key_file.read()
    print(
        ((
            int.from_bytes(cipher_content, sys.byteorder) ^ int.from_bytes(key_content, sys.byteorder)
        ).to_bytes(max(len(cipher_content), len(key_content)), sys.byteorder)).decode()
    )
