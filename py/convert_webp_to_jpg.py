from PIL import Image
import os

def convert_webp_to_jpg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file in os.listdir(input_folder):
        if file.lower().endswith(".webp"):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".jpg")
            
            with Image.open(input_path) as img:
                img = img.convert("RGB")
                img.save(output_path, "JPEG", quality=90)
                print(f"Converted: {file} -> {output_path}")

if __name__ == "__main__":
    input_folder = os.getcwd()  # Aktuelles Arbeitsverzeichnis als Eingangsordner
    output_folder = os.path.join(input_folder, "_processed")  # Ordner "_processed" für Ausgaben
    convert_webp_to_jpg(input_folder, output_folder)
