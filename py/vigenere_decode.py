from mylib import ALPHABET
from key_manager import load_vkey

encryptor = load_vkey()

def vigenere_decrypt_char(char, encryptor, key_index):
    if char.upper() not in ALPHABET:
        return char, key_index

    position_text = ALPHABET.find(char.upper())
    position_key = ALPHABET.find(encryptor[key_index % len(encryptor)].upper())
    decrypted_position = (position_text - position_key) % 26
    decrypted_char = ALPHABET[decrypted_position]

    next_key_index = (key_index + 1) % len(encryptor)
    return decrypted_char, next_key_index

def decode_string(encoded_string):
    key_index = 0
    decoded_string = ""

    for char in encoded_string:
        decrypted_char, key_index = vigenere_decrypt_char(char, encryptor, key_index)
        decoded_string += decrypted_char

    return decoded_string

if __name__ == "__main__":
    encoded_string = input("Gib den verschlüsselten String ein: ")
    decoded_string = decode_string(encoded_string)
    print(f"Dekodierter String: {decoded_string}")
