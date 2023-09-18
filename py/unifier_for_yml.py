import os
import logging

logging.basicConfig(level=logging.DEBUG, # Logger Config
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_file(file_path):
    logger.debug(f"file_path: {file_path}")
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1']
    logger.debug(f"List of encodings to try: {encodings}")
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                logger.debug(f"file_path: {file_path}")
                logger.debug(f"encoding: {encoding}")
                logger.debug(f"file.read: {file.read}")
                return file.read()
        except UnicodeDecodeError as e:
            logger.exception(e)
            continue
    return None

def combine_yml_files(output_file, search_directory):
    if not os.path.exists(search_directory):
        raise FileNotFoundError(f"The directory '{search_directory}' does not exist.")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(search_directory):
            for file in files:
                if file.endswith('.yml'):
                    file_path = os.path.join(root, file)
                    content = read_file(file_path)
                    if content:
                        outfile.write(content)
                        outfile.write('\n')  # Optional: Adds a newline between files

if __name__ == "__main__":
    output_file = 'combined.yml'
    search_directory = './localization/english'
    try:
        combine_yml_files(output_file, search_directory)
        logger.info(f'All .yml files in {search_directory} have been combined into {output_file}')
    except FileNotFoundError as e:
        logger.exception(e)
