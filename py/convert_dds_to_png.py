import os
from PIL import Image

def convert_dds_to_png():
    # Hole das aktuelle Arbeitsverzeichnis
    cwd = os.getcwd()
    
    # Liste alle Dateien im aktuellen Verzeichnis auf
    files = os.listdir(cwd)
    
    # Filtere nur die DDS-Dateien heraus
    dds_files = [file for file in files if file.lower().endswith('.dds')]
    
    for dds_file in dds_files:
        # Öffne die DDS-Datei
        with Image.open(dds_file) as img:
            # Konvertiere und speichere als PNG
            png_file = f"{os.path.splitext(dds_file)[0]}.png"
            img.save(png_file)
            print(f"Konvertiert: {dds_file} -> {png_file}")

if __name__ == "__main__":
    convert_dds_to_png()
