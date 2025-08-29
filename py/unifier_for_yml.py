import os
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_file(file_path):
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                logger.debug(f"Erfolgreich gelesen: {file_path} mit Encoding {encoding}")
                return file.read()
        except UnicodeDecodeError:
            logger.warning(f"Fehlgeschlagenes Encoding für Datei {file_path}: {encoding}")
            continue
        except Exception as e:
            logger.error(f"Fehler beim Lesen von {file_path}: {e}")
            return None
    return None

def find_and_read_version(start_dir):
    for root, dirs, files in os.walk(start_dir):
        if 'metadata.json' in files:
            metadata_path = os.path.join(root, 'metadata.json')
            try:
                with open(metadata_path, 'r', encoding='utf-8') as meta_file:
                    metadata = json.load(meta_file)
                    version = metadata.get('version')
                    if version:
                        logger.info(f"Gefundene Version: {version} in {metadata_path}")
                        return version
            except Exception as e:
                logger.error(f"Fehler beim Lesen der metadata.json: {e}")
                continue
    logger.error("Keine metadata.json mit 'version' gefunden.")
    return None

def combine_yml_files(output_file, search_directory):
    if not os.path.exists(search_directory):
        logger.error(f"Das Verzeichnis '{search_directory}' existiert nicht!")
        raise FileNotFoundError(f"Das Verzeichnis '{search_directory}' existiert nicht.")

    skip_files = {'scripts.txt', 'localizations.txt'}

    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        for root, _, files in os.walk(search_directory):
            for file in files:
                if file.endswith('.yml') and file.lower() not in skip_files:
                    file_path = os.path.join(root, file)
                    content = read_file(file_path)
                    if content:
                        outfile.write(f"# Datei: {os.path.relpath(file_path, search_directory)}\n")
                        outfile.write(content + '\n')
                        logger.info(f"Inhalt von {file_path} hinzugefügt.")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    search_directory = os.path.join(script_dir, "localization", "english")
    version = find_and_read_version(script_dir)
    if not version:
        logger.error("Abbruch: Keine gültige Version gefunden.")
        return
    output_file = os.path.join(script_dir, f"localizations_{version}.txt")

    try:
        logger.info(f"Starte das Zusammenführen von .yml-Dateien in {search_directory}")
        combine_yml_files(output_file, search_directory)
        logger.info(f"Alle .yml-Dateien wurden in {output_file} kombiniert.")
    except FileNotFoundError:
        logger.exception("Fehlgeschlagen: Verzeichnis nicht gefunden.")
    except Exception as e:
        logger.exception(f"Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()
