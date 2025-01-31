from cryptography.fernet import Fernet

# Einen neuen geheimen Schlüssel erzeugen
secret_key = Fernet.generate_key()

print(f"Speichere diesen SECRET_KEY sicher: {secret_key.decode()}")

# OPTIONAL: Den Schlüssel in einer Datei speichern
with open("secret.key", "wb") as key_file:
    key_file.write(secret_key)
