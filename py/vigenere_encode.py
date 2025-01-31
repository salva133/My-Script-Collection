from mylib import ALPHABET
from cryptography.fernet import Fernet

enc_path = "F:/MyScriptCollection/py/vkey.enc"
secret_path = "F:/MyScriptCollection/py/secret.key"

def load_secret_key():
    with open(secret_path, "rb") as key_file:
        return key_file.read()

def load_vkey():
    with open(enc_path, "rb") as f:
        encrypted_vkey = f.read()
    cipher = Fernet(load_secret_key())
    return cipher.decrypt(encrypted_vkey).decode()

encryptor = load_vkey()

def vigenere_encrypt_char(char, encryptor, key_index):
    if char.upper() not in ALPHABET:
        return char, key_index

    position_text = ALPHABET.find(char.upper())
    position_key = ALPHABET.find(encryptor[key_index % len(encryptor)].upper())
    encrypted_position = (position_text + position_key) % 26
    encrypted_char = ALPHABET[encrypted_position]

    next_key_index = (key_index + 1) % len(encryptor)
    return encrypted_char, next_key_index

def encode_string(plain_text):
    key_index = 0
    encoded_string = ""

    for char in plain_text:
        encrypted_char, key_index = vigenere_encrypt_char(char, encryptor, key_index)
        encoded_string += encrypted_char

    return encoded_string

if __name__ == "__main__":
    plain_text = input("Gib den Klartext ein: ")
    encoded_string = encode_string(plain_text)
    print(f"Verschlüsselter String: {encoded_string}")
