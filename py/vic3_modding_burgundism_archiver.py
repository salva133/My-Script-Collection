import os
import zipfile
import shutil
from pathlib import Path

# KONFIGURATION
MOD_FOLDER = r"C:\Users\Asus\Documents\Paradox Interactive\Victoria 3\mod\Burgundism"
PARENT_FOLDER = str(Path(MOD_FOLDER).parent)

IGNORE_FILES = {'.py', '.sh', 'LICENSE'}
IGNORE_FOLDERS = {'.git', 'sfx'}

def should_ignore(path: Path):
    if path.name in IGNORE_FOLDERS and path.is_dir():
        return True
    if path.name.startswith('.git'):
        return True
    if path.suffix in IGNORE_FILES and path.is_file():
        return True
    return False

def create_zip(source_folder, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            # Folders filtern
            dirs[:] = [d for d in dirs if not should_ignore(Path(root) / d)]
            for file in files:
                filepath = Path(root) / file
                if not should_ignore(filepath):
                    arcname = filepath.relative_to(source_folder)
                    zipf.write(filepath, arcname)

def extract_zip(zip_path, target_folder):
    with zipfile.ZipFile(zip_path, "r") as zipf:
        zipf.extractall(target_folder)

if __name__ == "__main__":
    mod_name = Path(MOD_FOLDER).name
    zip_name = f"{mod_name}.zip"
    zip_path = Path(PARENT_FOLDER) / zip_name

    if not zip_path.exists():
        print(f"Erstelle Paket: {zip_name}")
        create_zip(MOD_FOLDER, zip_path)
        print("Paket erstellt.")
    else:
        print(f"Paket {zip_name} existiert bereits, entpacke in Zielordner.")
        extract_zip(zip_path, MOD_FOLDER)
        print("Entpackt. Keine weiteren Aktionen.")
