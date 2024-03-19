"""
Script Name: sort_images.py
Description: This script sorts image files in the current directory based on specific substrings within their filenames. If a filename contains a predefined substring, the script moves the file to a corresponding directory. This tool is particularly useful for organizing a large number of image files into categorized folders.

Functions:
    move_files(substring, directory) - Checks for the existence of a target directory and moves files containing a specific substring into that directory.

Usage:
    1. Define the substring and corresponding directory names within the script.
    2. Run the script in the directory containing the image files to be sorted.
    3. The script will automatically create the necessary directories (if they do not exist) and move the matching files into them.

Note:
    The script is set up for dry runs initially; make sure to modify it according to your directory and file management needs.
"""


import os
import shutil
from tqdm import tqdm


def move_files(substring, directory):
    # Überprüfe, ob der Ordner existiert, wenn nicht, erstelle ihn
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Erstelle eine Liste aller Dateien im Verzeichnis
    files = os.listdir()

    # Erstelle einen Fortschrittsbalken
    progress = tqdm(
        total=len(files), desc=f"Verschiebe Dateien mit '{substring}'", ncols=100
    )

    # Durchsuche das aktuelle Verzeichnis
    for filename in files:
        # Versuche, die Datei zum Lesen zu öffnen
        try:
            with open(filename, "r") as file:
                pass
        except IOError:
            print(
                f"Die Datei {filename} wird gerade von einem anderen Prozess verwendet und kann nicht verschoben werden."
            )
            progress.update()
            continue  # überspringt das Verschieben dieser Datei

        # Wenn der Dateiname den Teilstring enthält, verschiebe die Datei in den entsprechenden Ordner
        if substring in filename:
            shutil.move(filename, os.path.join(directory, filename))

        # Aktualisiere den Fortschrittsbalken
        progress.update()

    # Schließe den Fortschrittsbalken am Ende
    progress.close()


# Verschiebe Dateien basierend auf den gegebenen Teilstrings in die entsprechenden Ordner
move_files("GPEN", "GPEN")
move_files("COMP", "COMP")
move_files("face", "face")
