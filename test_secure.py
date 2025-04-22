from secure_crypto import encrypt_file, decrypt_file

if __name__ == "__main__":
    file_path = "sample.txt"
    password = input("🔑 Enter password to encrypt/decrypt: ")

    # Encrypt
    encrypted_path = encrypt_file(file_path, password)

    # Decrypt
    decrypt_file(encrypted_path, password)
