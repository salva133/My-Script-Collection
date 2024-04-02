from mylib import ALPHABET
from mylib import VKEY as encryptor

def vigenere_encrypt_char(char, encryptor, key_index):
    if char.upper() not in ALPHABET:
        return char, key_index
    
    position_text = ALPHABET.find(char.upper())
    position_key = ALPHABET.find(encryptor[key_index % len(encryptor)].upper())
    encrypted_position = (position_text + position_key) % 26
    encrypted_char = ALPHABET[encrypted_position]
    
    next_key_index = (key_index + 1) % len(encryptor)
    return encrypted_char, next_key_index

def main():
    key_index = 0
    print("Vigenère-Verschlüsselung gestartet. Drücke Enter zum Zurücksetzen, zweimal Enter zum Beenden.")

    while True:
        char = input("Gib einen Buchstaben ein: ")
        
        if char == "":
            if key_index == 0:
                print("Schlüssel wird geleert und Programm beendet.")
                encryptor = ""
                break
            else:
                print("Schlüsselindex zurückgesetzt.")
                key_index = 0
                continue
        
        encrypted_char, key_index = vigenere_encrypt_char(char, encryptor, key_index)
        print(f"Verschlüsselter Buchstabe: {encrypted_char}")

if __name__ == "__main__":
    main()