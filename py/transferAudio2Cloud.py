import os
import shutil
import time
import zipfile

ziel_verzeichnis = "E:\\Music & Stuff\\FL Studio"
backup_verzeichnis = "E:\\Music & Stuff\\FL Studio Backup"
debug = True

def debug_print(message):
    if debug:
        print(message)

def erstelle_backup(ziel):
    try:
        backup_name = os.path.join(backup_verzeichnis, 'FL_Studio_Backup.zip')
        with zipfile.ZipFile(backup_name, 'w') as backup_zip:
            for root, dirs, files in os.walk(ziel):
                for file in files:
                    backup_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(ziel, '..')))
        debug_print(f"Backup erstellt unter: {backup_name}")
    except Exception as e:
        debug_print(f"Fehler beim Erstellen des Backups: {e}")

def stelle_backup_wieder_her(backup_pfad, ziel):
    try:
        with zipfile.ZipFile(backup_pfad, 'r') as file:
            file.extractall(ziel)
        debug_print(f"Backup wiederhergestellt von: {backup_pfad}")
    except Exception as e:
        debug_print(f"Fehler beim Wiederherstellen des Backups: {e}")

def erstelle_verzeichnis(verzeichnis):
    try:
        if os.path.exists(verzeichnis):
            if os.listdir(verzeichnis):
                debug_print(f"Verzeichnis existiert und ist nicht leer: {verzeichnis}")
                erstelle_backup(verzeichnis)
                for filename in os.listdir(verzeichnis):
                    file_path = os.path.join(verzeichnis, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                debug_print(f"Inhalt von {verzeichnis} gelöscht")
            else:
                debug_print(f"Verzeichnis existiert, ist aber leer: {verzeichnis}")
        else:
            os.makedirs(verzeichnis)
            debug_print(f"Verzeichnis erstellt: {verzeichnis}")
    except Exception as e:
        debug_print("Auf das Verzeichnis konnte nicht zugegriffen werden. Ist die Platte vielleicht noch gesperrt?")
        debug_print(f"Fehler: {e}")
        time.sleep(5)
        exit()

def kopiere_audiodateien(cwd, ziel):
    try:
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith(('.mp3', '.wav', '.flac')):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(ziel, file)
                    try:
                        shutil.copy(source_path, destination_path)
                        debug_print(f"Kopiert: {source_path} -> {destination_path}")
                    except Exception as e:
                        debug_print(f"Fehler beim Kopieren der Datei {file}. Grund: {e}")
                        raise
    except Exception as e:
        debug_print(f"Ein Fehler trat auf während des Kopierprozesses: {e}")
        raise

def main():
    try:
        erstelle_verzeichnis(ziel_verzeichnis)
        kopiere_audiodateien(os.getcwd(), ziel_verzeichnis)
        debug_print("Kopieroperation abgeschlossen.")
    except Exception as e:
        debug_print(f'Fehler beim Kopiervorgang: {e}')
        debug_print('Stelle ursprünglichen Zustand aus Backup wieder her...')
        stelle_backup_wieder_her(os.path.join(backup_verzeichnis, 'FL_Studio_Backup.zip'), ziel_verzeichnis)
        debug_print('Wiederherstellung abgeschlossen.')

if __name__ == "__main__":
    main()
