from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

def derive_key(password, salt=None):
    salt = salt or get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=100000)
    return key, salt

def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    key, salt = derive_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(salt + iv + ciphertext)

    print(f"✅ Encrypted: {encrypted_file_path}")
    return encrypted_file_path

def decrypt_file(encrypted_file_path, password):
    with open(encrypted_file_path, 'rb') as f:
        data = f.read()

    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]
    key, _ = derive_key(password, salt)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    decrypted_file_path = encrypted_file_path.replace(".enc", "_decrypted.txt")
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

    print(f"✅ Decrypted: {decrypted_file_path}")
    return decrypted_file_path
