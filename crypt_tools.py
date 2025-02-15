from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def generate_keys():
    key = os.urandom(32)
    iv = os.urandom(16)
    with open('keys/aes_key.bin', 'wb') as key_file:
        key_file.write(key)
    with open('keys/aes_iv.bin', 'wb') as iv_file:
        iv_file.write(iv)
    return key, iv

def load_keys():
    with open('keys/aes_key.bin', 'rb') as key_file:
        key = key_file.read()
    with open('keys/aes_iv.bin', 'rb') as iv_file:
        iv = iv_file.read()
    return key, iv

def encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    return encrypted_data

def decrypt(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode()

if __name__ == "__main__":
    key, iv = generate_keys()
    print("Chaves geradas.")