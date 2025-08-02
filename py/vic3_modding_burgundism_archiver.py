import os
import zipfile
import shutil
from pathlib import Path
import tempfile
import logging
import sys

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("V3PackScript")

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
    temp_backup_dir = Path(tempfile.mkdtemp(prefix="v3mod_backup_"))
    logger.info(f"Temporäres Backup-Verzeichnis: {temp_backup_dir}")

    packed_paths = []

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_folder):
                root_path = Path(root)
                # Ordner iterieren (kopiere dirs, weil während Iteration verändert)
                for d in list(dirs):
                    dir_path = root_path / d
                    if should_pack(dir_path):
                        backup_path = temp_backup_dir / dir_path.relative_to(source_folder)
                        logger.info(f"Verschiebe Ordner '{dir_path}' nach Backup '{backup_path}'")
                        shutil.move(str(dir_path), str(backup_path))
                        packed_paths.append((dir_path, backup_path, True))
                        # Ordner packen (aus Backup-Verzeichnis)
                        for dir_root, _, dir_files in os.walk(backup_path):
                            for f in dir_files:
                                file_path = Path(dir_root) / f
                                rel_path = file_path.relative_to(temp_backup_dir)
                                logger.info(f"Packe Datei aus Backup: {file_path}")
                                zipf.write(file_path, rel_path)
                        dirs.remove(d)
                # Dateien iterieren
                for f in files:
                    file_path = root_path / f
                    if should_pack(file_path):
                        backup_path = temp_backup_dir / file_path.relative_to(source_folder)
                        backup_path.parent.mkdir(parents=True, exist_ok=True)
                        logger.info(f"Verschiebe Datei '{file_path}' nach Backup '{backup_path}'")
                        shutil.move(str(file_path), str(backup_path))
                        packed_paths.append((file_path, backup_path, False))
                        rel_path = backup_path.relative_to(temp_backup_dir)
                        logger.info(f"Packe Datei aus Backup: {backup_path}")
                        zipf.write(backup_path, rel_path)
        # Erfolgreich: Backup löschen
        logger.info("Packen erfolgreich, lösche temporäres Backup.")
        shutil.rmtree(temp_backup_dir)
        return True
    except Exception as e:
        logger.error(f"Fehler beim Packen: {e}")
        # Restore alles aus dem Backup-Verzeichnis
        for orig_path, backup_path, is_dir in packed_paths[::-1]:
            if backup_path.exists():
                logger.info(f"Stelle '{orig_path}' aus Backup '{backup_path}' wieder her.")
                # Existiert original schon wieder (z.B. bei Wiederholungen), dann vorher löschen
                if orig_path.exists():
                    if orig_path.is_dir():
                        shutil.rmtree(orig_path)
                    else:
                        orig_path.unlink()
                shutil.move(str(backup_path), str(orig_path))
        logger.info(f"Backup-Verzeichnis bleibt erhalten für manuelle Kontrolle: {temp_backup_dir}")
        return False

if __name__ == "__main__":
    mod_name = Path(MOD_FOLDER).name
    zip_name = f"{mod_name}_TO_PACK.zip"
    zip_path = Path(PARENT_FOLDER) / zip_name

    if not zip_path.exists():
        logger.info(f"Packe und entferne ausgewählte Dateien/Ordner in: {zip_name}")
        result = pack_and_remove_selected(MOD_FOLDER, zip_path)
        if result:
            logger.info("Fertig: Ausgewählte Dateien gepackt und entfernt.")
        else:
            logger.error("Vorgang fehlgeschlagen. Alles wurde zurückgerollt.")
    else:
        logger.info(f"Archiv {zip_name} existiert bereits. Keine Aktion durchgeführt.")
