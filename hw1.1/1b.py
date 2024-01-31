with open("3/forstudents/b/ciphertext1.bin", "rb") as cipher1_file, open(
    "3/forstudents/b/ciphertext2.bin", "rb"
) as cipher2_file, open("3/forstudents/b/plaintext1.txt", "r") as plain_unknown_file:
    cipher1_content = cipher1_file.read()
    cipher2_content = cipher2_file.read()
    plain_unknown_content = plain_unknown_file.read()

    possible_key = (
        int.from_bytes(cipher1_content, "big")
        ^ int.from_bytes(bytes(plain_unknown_content, "utf-8"), "big")
    ).to_bytes(max(len(cipher1_content), len(plain_unknown_content)), "big")
    print(
        (
            (
                int.from_bytes(cipher2_content, "big")
                ^ int.from_bytes(possible_key, "big")
            ).to_bytes(max(len(cipher2_content), len(possible_key)), "big")
        ).decode("latin-1")
    )
