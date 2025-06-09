import os
import secrets
from mylib import ALPHABET

DATEINAME = "secret.key"

def generate_vkey(laenge=32):
    """Erstellt einen neuen zufälligen Vigenère-Schlüssel der angegebenen Länge."""
    return ''.join(secrets.choice(ALPHABET) for _ in range(laenge))

def save_vkey(key, dateiname=DATEINAME):
    """Speichert den Vigenère-Schlüssel in einer Datei."""
    with open(dateiname, "w") as f:
        f.write(key)

def load_vkey(dateiname=DATEINAME):
    """Lädt den Vigenère-Schlüssel aus der Datei oder generiert einen neuen, falls nicht vorhanden."""
    if os.path.exists(dateiname):
        with open(dateiname, "r") as f:
            key = f.read().strip()
    else:
        key = generate_vkey()
        save_vkey(key, dateiname)
        print(f"Neuer Vigenère-Schlüssel generiert und in {dateiname} gespeichert.")
    return key
