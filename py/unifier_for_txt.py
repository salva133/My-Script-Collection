import os
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_file(file_path):
    logger.debug(f"Reading file: {file_path}")
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                logger.debug(f"Successfully read file with encoding: {encoding}")
                return file.read()
        except UnicodeDecodeError:
            logger.error(f"Failed to read file with encoding: {encoding}")
            continue
    logger.debug(f"Failed to read file: {file_path} with any known encoding")
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
                logger.exception(f"Fehler beim Lesen der metadata.json: {e}")
                continue
    logger.error("Keine metadata.json mit 'version' gefunden.")
    return None

def combine_txt_files(output_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logger.debug(f"Script directory: {script_dir}")
    logger.debug(f"Output file: {output_file}")

    skip_files = {'scripts.txt', 'localizations.txt', 'steam_desc.txt'}

    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        logger.debug(f"Opened output file: {output_file}")
        for root, dirs, files in os.walk(script_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            logger.debug(f"Walking directory: {root}")
            for file in files:
                if (
                    file.endswith('.txt')
                    and file.lower() not in skip_files
                ):
                    file_path = os.path.join(root, file)
                    logger.debug(f"Processing file: {file_path}")
                    content = read_file(file_path)
                    if content:
                        outfile.write(f'Filename: {file}\n')
                        outfile.write(content)
                        outfile.write('\n')
                        logger.info(f"Wrote content of file: {file_path} to output file")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    version = find_and_read_version(script_dir)
    if not version:
        logger.error("Abbruch: Keine gültige Version gefunden.")
        return
    output_file = os.path.join(script_dir, f'scripts_{version}.txt')
    logger.info("Starte das Kombinieren der TXT-Dateien")
    combine_txt_files(output_file)
    logger.info(f'Alle .txt Dateien wurden in {output_file} kombiniert.')

if __name__ == "__main__":
    main()
