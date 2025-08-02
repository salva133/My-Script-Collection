import os
import shutil
import time
import zipfile
import logging
import hashlib

debug = True
quell_verzeichnis = r"C:\Users\Asus\Documents\Image-Line\FL Studio\Projects"
ziel_verzeichnis = r"C:\Users\Asus\Proton Drive\hans.rudi.giger\My files\FL Studio Tracks"
backup_verzeichnis = r"C:\Users\Asus\Proton Drive\hans.rudi.giger\My files\FL Studio Tracks Backup"
file_extensions = ('.mp3', '.wav')

logging.basicConfig(level=logging.DEBUG, # Logger Config
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def erstelle_backup(ziel):
def files_are_identical(file1, file2):
    if not os.path.exists(file2):
        return False
    if os.path.getsize(file1) != os.path.getsize(file2):
        return False
    def get_hash(path):
        hash_obj = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    return get_hash(file1) == get_hash(file2)

def create_backup(target):
    try:
        os.makedirs(backup_verzeichnis, exist_ok=True)
        ordnername = os.path.basename(os.path.normpath(ziel))
        backup_name = os.path.join(
            backup_verzeichnis,
            f"{ordnername}-Backup.zip"
        )
        with zipfile.ZipFile(backup_name, 'w') as backup_zip:
            for root, dirs, files in os.walk(ziel):
                for file in files:
                    backup_zip.write(
                        os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file), ziel)
                    )
        logger.debug(f"Backup erstellt unter: {backup_name}")
    except Exception as e:
        logger.exception(f"Fehler beim Erstellen des Backups: {e}")

def stelle_backup_wieder_her_fuer_ziel(ziel):
    try:
        ordnername = os.path.basename(os.path.normpath(ziel))
        backup_pfad = os.path.join(backup_verzeichnis, f"{ordnername}-Backup.zip")
        if not os.path.exists(backup_pfad):
            logger.error(f"Kein Backup gefunden unter: {backup_pfad}")
            return
        with zipfile.ZipFile(backup_pfad, 'r') as file:
            file.extractall(ziel)
        logger.debug(f"Backup wiederhergestellt von: {backup_pfad}")
    except Exception as e:
        logger.exception(f"Fehler beim Wiederherstellen des Backups: {e}")

def erstelle_verzeichnis(verzeichnis):
    try:
        if os.path.exists(verzeichnis):
            if os.listdir(verzeichnis):
                logger.debug(f"Verzeichnis existiert und ist nicht leer: {verzeichnis}")
                erstelle_backup(verzeichnis)
                for filename in os.listdir(verzeichnis):
                    file_path = os.path.join(verzeichnis, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                logger.debug(f"Inhalt von {verzeichnis} gelöscht")
            else:
                logger.debug(f"Verzeichnis existiert, ist aber leer: {verzeichnis}")
        else:
            os.makedirs(verzeichnis)
            logger.debug(f"Verzeichnis erstellt: {verzeichnis}")
    except Exception as e:
        logger.exception("Auf das Verzeichnis konnte nicht zugegriffen werden. Ist die Platte vielleicht noch gesperrt?")
        logger.exception(f"Fehler: {e}")
        time.sleep(5)
        exit()

def kopiere_audiodateien(cwd, ziel):
    try:
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith(file_extensions):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(ziel, file)
                    try:
                        if os.path.exists(destination_path):
                            if files_are_identical(source_path, destination_path):
                                logger.debug(f"Skipped (identical): {source_path} -> {destination_path}")
                                continue  # Skip identical file
                        shutil.copy(source_path, destination_path)
                        logger.debug(f"Kopiert: {source_path} -> {destination_path}")
                    except Exception as e:
                        logger.exception(f"Fehler beim Kopieren der Datei {file}. Grund: {e}")
                        raise
    except Exception as e:
        logger.exception(f"Ein Fehler trat auf während des Kopierprozesses: {e}")
        raise

def main():
    try:
        erstelle_verzeichnis(ziel_verzeichnis)
        kopiere_audiodateien(quell_verzeichnis, ziel_verzeichnis)
        logger.debug("Kopieroperation abgeschlossen.")
    except Exception as e:
        logger.exception(f'Fehler beim Kopiervorgang: {e}')
        logger.exception('Stelle ursprünglichen Zustand aus Backup wieder her...')
        stelle_backup_wieder_her_fuer_ziel(ziel_verzeichnis)
        logger.exception('Wiederherstellung abgeschlossen.')

if __name__ == "__main__":
    main()
