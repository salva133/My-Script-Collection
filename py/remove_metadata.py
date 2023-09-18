import os
import subprocess
import json
import shutil
import logging

logging.basicConfig(level=logging.DEBUG, # Logger Config
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_media_files(directory):
    media_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.mp4', '.mov', '.avi', '.mkv']
    media_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in media_extensions):
                media_files.append(os.path.join(root, file))
    return media_files

def remove_metadata(file_path):
    try:
        subprocess.run(['exiftool', '-all=', file_path], check=True)
        print(f'Metadata removed from {file_path}')
        move_original_file(file_path)  # Move the .original file after removing metadata
    except subprocess.CalledProcessError as e:
        print(f'Error removing metadata from {file_path}: {e}')

def verify_metadata_removal(file_path):
    try:
        result = subprocess.run(['exiftool', '-json', file_path], capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)
        if metadata and metadata[0]:  # Checking if there is any metadata left
            keys = list(metadata[0].keys())
            # Exclude default keys that are always present
            keys_to_exclude = ['SourceFile', 'ExifToolVersion', 'FileName', 'Directory', 'FileSize', 'FileModifyDate', 'FileAccessDate', 'FileInodeChangeDate', 'FilePermissions']
            remaining_keys = [key for key in keys if key not in keys_to_exclude]
            if remaining_keys:
                print(f'Metadata still present in {file_path}: {remaining_keys}')
            else:
                print(f'No metadata present in {file_path}. Verification successful.')
    except subprocess.CalledProcessError as e:
        print(f'Error verifying metadata removal for {file_path}: {e}')

def move_original_file(file_path):
    original_file = file_path + '_original'
    if os.path.exists(original_file):
        original_folder = os.path.join(os.path.dirname(file_path), '.original')
        os.makedirs(original_folder, exist_ok=True)
        destination_path = os.path.join(original_folder, os.path.basename(original_file))
        
        # If a file with the same name exists, overwrite it
        if os.path.exists(destination_path):
            os.remove(destination_path)
        
        shutil.move(original_file, destination_path)
        print(f'Moved original file to {destination_path}')

def main():
    cwd = os.getcwd()
    media_files = get_media_files(cwd)
    for file in media_files:
        remove_metadata(file)
        verify_metadata_removal(file)
    print('Metadata removal and verification complete.')

if __name__ == '__main__':
    main()
