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

def move_to_processed(file_path, processed_dir="_processed"):
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    base_name = os.path.basename(file_path)
    new_path = os.path.join(processed_dir, base_name)

    counter = 1
    while os.path.exists(new_path):
        base, ext = os.path.splitext(base_name)
        new_path = os.path.join(processed_dir, f"{base}_{counter}{ext}")
        counter += 1

    os.rename(file_path, new_path)
    print(f"Datei verschoben: {file_path} zu {new_path}")

# Durchlaufen aller Dateien im aktuellen Verzeichnis
for file in os.listdir('.'):
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Erstellen des Ausgabedateinamens
        output_file = f"{os.path.splitext(file)[0]}.dds"
        
        # Konvertierung der Datei
        print(f"Konvertiere: {file}")
        convert_to_dds(file, output_file)

        # Verschieben der verarbeiteten Datei
        move_to_processed(file)

print("Konvertierungsprozess abgeschlossen.")
