from PIL import Image
import os

def convert_png_to_jpg(directory):
    # Hole alle Dateien im Verzeichnis
    files = [f for f in os.listdir(directory) if f.endswith('.png')]
    
    for file in files:
        try:
            # Lade das PNG-Bild
            with Image.open(file) as img:
                # Konvertiere das Bild in RGB (notwendig für JPG)
                rgb_img = img.convert('RGB')
                
                # Bestimme den neuen Dateinamen
                new_file = os.path.splitext(file)[0] + '.jpg'
                
                # Speichere das Bild als JPG mit 90 % Qualität
                rgb_img.save(new_file, 'JPEG', quality=95)
                print(f"Konvertiert: {file} -> {new_file}")
        except Exception as e:
            print(f"Fehler bei {file}: {e}")

if __name__ == "__main__":
    # Aktuelles Arbeitsverzeichnis
    cwd = os.getcwd()
    convert_png_to_jpg(cwd)
