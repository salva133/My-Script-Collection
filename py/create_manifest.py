import os
import subprocess
from collections import defaultdict

# Liste erlaubter Audioformate
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"}

def create_manifest(output_file="manifest.txt"):
    seen_files = defaultdict(list)  # Dictionary zur Erfassung von doppelten Namen

    with open(output_file, "w", encoding="utf-8") as f:
        for root, _, files in os.walk(os.getcwd()):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in AUDIO_EXTENSIONS:
                    rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                    rel_path_no_ext = os.path.splitext(rel_path)[0]
                    f.write(rel_path_no_ext + "\n")

                    # Speichert Dateiname (ohne Pfad) für doppelte Einträge
                    seen_files[file].append(rel_path)

        # Redundante Namen am Ende des Manifests ausgeben
        f.write("\n# Redundante Dateinamen:\n")
        for name, paths in seen_files.items():
            if len(paths) > 1:
                f.write(f"{name} ({len(paths)}x):\n")
                for path in paths:
                    f.write(f"  - {path}\n")

def run_enumeration_script():
    try:
        script_path = os.path.join(os.getcwd(), "enumerate_all_files_here_plus_in_subdirs.py")
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(f"Fehler beim Ausführen von {script_path}: {e}")

if __name__ == "__main__":
    run_enumeration_script()
    create_manifest()
    print("Manifest wurde erstellt: manifest.txt (überschrieben falls vorhanden)")
