import os
import shutil
import time
import zipfile
import logging

debug = True
ziel_verzeichnis = "E:\\Music & Stuff\\FL Studio"
backup_verzeichnis = "E:\\Music & Stuff\\FL Studio Backup"
file_extensions = ('.mp3', '.wav', '.flac')

logging.basicConfig(level=logging.DEBUG, # Logger Config
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

''' Muss noch überarbeitet werden
def erstelle_backup(ziel):
    try:
        backup_name = os.path.join(backup_verzeichnis, 'FL_Studio_Backup.zip')
        with zipfile.ZipFile(backup_name, 'w') as backup_zip:
            for root, dirs, files in os.walk(ziel):
                for file in files:
                    backup_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(ziel, '..')))
        logger.debug(f"Backup erstellt unter: {backup_name}")
    except Exception as e:
        logger.exception(f"Fehler beim Erstellen des Backups: {e}")
'''

def stelle_backup_wieder_her(backup_pfad, ziel):
    try:
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
                # erstelle_backup(verzeichnis) ### Wurde deaktiviert
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
        kopiere_audiodateien(os.getcwd(), ziel_verzeichnis)
        logger.debug("Kopieroperation abgeschlossen.")
    except Exception as e:
        logger.exception(f'Fehler beim Kopiervorgang: {e}')
        logger.exception('Stelle ursprünglichen Zustand aus Backup wieder her...')
        stelle_backup_wieder_her(os.path.join(backup_verzeichnis, 'FL_Studio_Backup.zip'), ziel_verzeichnis)
        logger.exception('Wiederherstellung abgeschlossen.')

if __name__ == "__main__":
    main()
