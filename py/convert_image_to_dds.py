"""
Script Name: convert_image_to_dds.py
Description: This script converts image files from common formats (such as PNG, JPG, JPEG, BMP, and GIF) to the DDS format. It is designed to process all suitable image files within the current directory, converting each one individually and saving the results as new files with the same base filenames but with the .dds extension.

Functions:
    convert_to_dds(input_image_path, output_image_path) - Converts a single image file from its original format to DDS format using the imageio library.

Workflow:
    1. Iterate over all files in the current directory.
    2. Check each file to see if it ends with one of the supported image extensions.
    3. Convert supported image files to DDS format, maintaining the original base filename.
"""


import os
from PIL import Image
import imageio

def convert_to_dds(input_image_path, output_image_path):
    try:
        # Bild mit Pillow öffnen
        image = Image.open(input_image_path)

        # Bild als DDS speichern
        imageio.imwrite(output_image_path, image, format='dds')
        print(f"Erfolgreich konvertiert: {input_image_path} zu {output_image_path}")
    except Exception as e:
        print(f"Fehler beim Konvertieren von {input_image_path}: {e}")

# Durchlaufen aller Dateien im aktuellen Verzeichnis
for file in os.listdir('.'):
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Erstellen des Ausgabedateinamens
        output_file = f"{os.path.splitext(file)[0]}.dds"
        
        # Konvertierung der Datei
        print(f"Konvertiere: {file}")
        convert_to_dds(file, output_file)

print("Konvertierungsprozess abgeschlossen.")
