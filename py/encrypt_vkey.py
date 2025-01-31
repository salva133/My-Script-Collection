from cryptography.fernet import Fernet

# SECRET_KEY aus Datei laden oder manuell einfügen
with open("secret.key", "rb") as key_file:
    SECRET_KEY = key_file.read()

cipher = Fernet(SECRET_KEY)

# Ersetze dies mit deinem tatsächlichen Vigenère-Schlüssel
VKEY = KEY

# VKEY verschlüsseln
encrypted_vkey = cipher.encrypt(VKEY.encode())

# In Datei speichern
with open("vkey.enc", "wb") as f:
    f.write(encrypted_vkey)

print("VKEY wurde erfolgreich verschlüsselt und gespeichert.")
