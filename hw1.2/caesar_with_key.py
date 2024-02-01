with open("3/withkey/caesarkey.txt", "r") as caesar_key_file, open(
    "3/withkey/ciphertext.txt", "r"
) as caesar_cipher_file:
    caesar_key_content = caesar_key_file.read()
    caesar_cipher_content = caesar_cipher_file.read()

    key_shift = int(caesar_key_content.split()[-1])
    print("key shift", key_shift)
    
    caesar_plaintext_content_left_shift = ""
    caesar_plaintext_content_right_shift = ""
    for char in caesar_cipher_content:
        caesar_plaintext_content_left_shift += chr(
            (ord(char) - ord("A") - key_shift) % 26 + ord("A")
        )
        caesar_plaintext_content_right_shift += chr(
            (ord(char) - ord("A") + key_shift) % 26 + ord("A")
        )

    print("left shift")
    print(caesar_plaintext_content_left_shift)
    print()
    print("right shift")
    print(caesar_plaintext_content_right_shift)
