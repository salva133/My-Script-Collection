import os
import re
from collections import defaultdict

# Liste erlaubter Audioformate
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"}

def extract_relevant_name(filename):
    """
    Extrahiert den relevanten Namensteil aus einem Dateinamen.
    Falls '(remastered)' oder '(cover)' vorkommen, werden sie entfernt.
    Falls kein '_' vorhanden ist, wird der gesamte Name ohne Dateiendung genutzt.
    """
    base_name, _ = os.path.splitext(filename)  # Entfernt Dateiendung

    # Entferne '(remastered)' oder '(cover)', falls vorhanden
    base_name = re.sub(r'\s*\((remastered|cover)\)', '', base_name, flags=re.IGNORECASE)

    # Falls ein Unterstrich vorhanden ist, alles nach dem ersten Unterstrich nutzen
    if "_" in base_name:
        return base_name.split("_", 1)[1].strip().lower()

    return base_name.strip().lower()  # Falls kein Unterstrich, den gesamten Namen nutzen

def create_manifest(output_file="manifest.txt"):
    seen_files = defaultdict(list)  # Dictionary zur Erfassung von Dateipfaden
    name_redundancies = defaultdict(list)  # Dictionary für redundante Namen

    with open(output_file, "w", encoding="utf-8") as f:
        for root, _, files in os.walk(os.getcwd()):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in AUDIO_EXTENSIONS:
                    rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                    rel_path_no_ext = os.path.splitext(rel_path)[0]
                    f.write(rel_path_no_ext + "\n")

                    # Originalname speichern
                    seen_files[file].append(rel_path)

                    # Prüfen auf redundante Namen
                    relevant_name = extract_relevant_name(file)
                    name_redundancies[relevant_name].append(rel_path)

        # Redundante Namen am Ende des Manifests ausgeben
        f.write("\n# Redundante Dateinamen:\n")
        for name, paths in name_redundancies.items():
            if len(paths) > 1:  # Nur wenn >1 Datei existiert
                f.write(f"{name} ({len(paths)}x):\n")
                for path in paths:
                    f.write(f"  - {path}\n")

    print("Manifest wurde erstellt: manifest.txt (überschrieben falls vorhanden)")

if __name__ == "__main__":
    create_manifest()
