import os
import zipfile
import shutil
from pathlib import Path

# KONFIGURATION
MOD_FOLDER = r"C:\Users\Asus\Documents\Paradox Interactive\Victoria 3\mod\Burgundism"
PARENT_FOLDER = str(Path(MOD_FOLDER).parent)

TO_PACK_FILES = {'.py', '.sh', 'LICENSE'}
TO_PACK_FOLDERS = {'.git', 'sfx'}

def should_pack(path: Path):
    if path.name in TO_PACK_FOLDERS and path.is_dir():
        return True
    if path.name.startswith('.git'):
        return True
    if path.suffix in TO_PACK_FILES and path.is_file():
        return True
    if path.name in TO_PACK_FILES and path.is_file():
        return True
    return False

def pack_and_remove_selected(source_folder, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            root_path = Path(root)
            for d in list(dirs):
                dir_path = root_path / d
                if should_pack(dir_path):
                    for dir_root, _, dir_files in os.walk(dir_path):
                        for f in dir_files:
                            file_path = Path(dir_root) / f
                            rel_path = file_path.relative_to(source_folder)
                            zipf.write(file_path, rel_path)
                    shutil.rmtree(dir_path)
                    dirs.remove(d)
            for f in files:
                file_path = root_path / f
                if should_pack(file_path):
                    rel_path = file_path.relative_to(source_folder)
                    zipf.write(file_path, rel_path)
                    file_path.unlink()

if __name__ == "__main__":
    mod_name = Path(MOD_FOLDER).name
    zip_name = f"{mod_name}_TO_PACK.zip"
    zip_path = Path(PARENT_FOLDER) / zip_name

    if not zip_path.exists():
        print(f"Packe und entferne ausgewählte Dateien/Ordner in: {zip_name}")
        pack_and_remove_selected(MOD_FOLDER, zip_path)
        print("Fertig: Ausgewählte Dateien gepackt und entfernt.")
    else:
        print(f"Archiv {zip_name} existiert bereits. Keine Aktion durchgeführt.")
