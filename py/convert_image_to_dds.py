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
