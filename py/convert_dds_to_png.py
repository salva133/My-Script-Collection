import os
from PIL import Image

# Verzeichnis mit DDS-Dateien
cwd = os.getcwd()

# Gehe durch alle Dateien im aktuellen Verzeichnis
for filename in os.listdir(cwd):
    if filename.endswith(".dds"):
        # Pfad zur DDS-Datei
        dds_path = os.path.join(cwd, filename)
        
        # Bild öffnen
        with Image.open(dds_path) as img:
            # Pfad zur PNG-Datei
            png_path = os.path.splitext(dds_path)[0] + ".png"
            
            # Bild als PNG speichern
            img.save(png_path, format="PNG")
            
        print(f"Konvertiert: {filename} -> {os.path.basename(png_path)}")

print("Konvertierung abgeschlossen.")
