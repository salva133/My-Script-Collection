import os
import logging

logging.basicConfig(level=logging.DEBUG, # Logger Config
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_file(file_path):
    logger.debug(f"Reading file: {file_path}")
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1']  # Liste der zu verwendenden Encodings
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                logger.debug(f"Successfully read file with encoding: {encoding}")
                return file.read()
        except UnicodeDecodeError:
            logger.exception(f"Failed to read file with encoding: {encoding}")
            continue
    logger.debug(f"Failed to read file: {file_path} with any known encoding")
    return None

def combine_txt_files(output_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Verzeichnis des Skripts
    logger.debug(f"Script directory: {script_dir}")
    logger.debug(f"Output file: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        logger.debug(f"Opened output file: {output_file}")
        for root, dirs, files in os.walk(script_dir):
            logger.debug(f"Walking directory: {root}")
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    logger.debug(f"Processing file: {file_path}")
                    content = read_file(file_path)
                    if content:
                        # Write filename before the content
                        outfile.write(f'Filename: {file}\n')
                        outfile.write(content)
                        outfile.write('\n')  # Optional: Fügt eine neue Zeile zwischen Dateien hinzu
                        logger.debug(f"Wrote content of file: {file_path} to output file")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Verzeichnis des Skripts
    parent_folder_name = os.path.basename(script_dir)  # Name des übergeordneten Verzeichnisses
    output_file = os.path.join(script_dir, f'{parent_folder_name}.txt')  # Ausgabedatei mit dem Namen des übergeordneten Verzeichnisses
    logger.info("Starting file combination process")
    combine_txt_files(output_file)
    logger.info(f'All .txt files have been combined into {output_file}')
