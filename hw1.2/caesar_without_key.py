with open("3/withoutkey/ciphertext.txt", "r") as caesar_cipher_file:
    caesar_cipher_content = caesar_cipher_file.read()

    for key_shift in range(1,14): # both left and right, 13x2=26
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
