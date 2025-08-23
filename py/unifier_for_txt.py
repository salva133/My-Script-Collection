import os
import logging

logging.basicConfig(level=logging.INFO, # Logger Config
                    format='%(asctime)s - %(levelname)s - %(message)s')
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
            logger.exception(f"Failed to read file with encoding: {encoding}")
            continue
    logger.debug(f"Failed to read file: {file_path} with any known encoding")
    return None

def combine_txt_files(output_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logger.debug(f"Script directory: {script_dir}")
    logger.debug(f"Output file: {output_file}")

    skip_files = {'scripts.txt', 'localizations.txt'}

    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        logger.debug(f"Opened output file: {output_file}")
        for root, dirs, files in os.walk(script_dir):
            # Verzeichnisse, die mit . beginnen, aus dirs entfernen (werden dann auch nicht weiter besucht)
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
                        logger.debug(f"Wrote content of file: {file_path} to output file")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'scripts.txt')  # Hartkodiert
    logger.info("Starting file combination process")
    combine_txt_files(output_file)
    logger.info(f'All .txt files have been combined into {output_file}')

if __name__ == "__main__":
    main()
