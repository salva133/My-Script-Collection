import os
import re

# Muster für erlaubte Zeichen (alphanumerische Zeichen, Unterstrich, Punkt und Leerzeichen)
pattern = re.compile(r'[^a-zA-Z0-9_. ]')

def process_filename(filename):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', 
                  re.sub(r'\s+', ' ', 
                         pattern.sub('', filename.replace("4K", "").replace("ASMR", ""))
                        ).strip())

# Funktion zum Durchlaufen von Verzeichnissen, auch rekursiv durch Subdirs
def rename_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Verarbeite den Dateinamen
            new_filename = process_filename(filename)
            
            # Vollständiger Pfad zu den Dateien
            old_file_path = os.path.join(root, filename)
            new_file_path = os.path.join(root, new_filename)
            
            # Umbenennen der Datei, wenn der neue Name anders ist
            if new_filename != filename:
                os.rename(old_file_path, new_file_path)
                print(f"Umbenannt: {old_file_path} -> {new_file_path}")

# Starte den Prozess im aktuellen Verzeichnis (inkl. Subdirs)
try:
    cwd = os.getcwd()
    rename_files_in_directory(cwd)
    print("Fertig!")
except Exception as e:
    print(f"Es ist ein Fehler aufgetreten: {e}")
finally:
    input("Programm beendet.")
