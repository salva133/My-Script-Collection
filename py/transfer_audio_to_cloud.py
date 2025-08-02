import os
import shutil
import time
import zipfile
import logging
import hashlib

debug = True
source_dir = r"C:\Users\Asus\Documents\Image-Line\FL Studio\Projects"
target_dir = r"C:\Users\Asus\Proton Drive\hans.rudi.giger\My files\FL Studio Tracks"
backup_dir = r"C:\Users\Asus\Proton Drive\hans.rudi.giger\My files\FL Studio Tracks Backup"
file_extensions = ('.mp3', '.wav')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        os.makedirs(backup_dir, exist_ok=True)
        folder_name = os.path.basename(os.path.normpath(target))
        backup_name = os.path.join(
            backup_dir,
            f"{folder_name}-Backup.zip"
        )
        with zipfile.ZipFile(backup_name, 'w') as backup_zip:
            for root, dirs, files in os.walk(target):
                for file in files:
                    backup_zip.write(
                        os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file), target)
                    )
        logger.debug(f"Backup created at: {backup_name}")
    except Exception as e:
        logger.exception(f"Error creating backup: {e}")

def restore_backup_for_target(target):
    try:
        folder_name = os.path.basename(os.path.normpath(target))
        backup_path = os.path.join(backup_dir, f"{folder_name}-Backup.zip")
        if not os.path.exists(backup_path):
            logger.error(f"No backup found at: {backup_path}")
            return
        with zipfile.ZipFile(backup_path, 'r') as file:
            file.extractall(target)
        logger.debug(f"Backup restored from: {backup_path}")
    except Exception as e:
        logger.exception(f"Error restoring backup: {e}")

def create_directory(directory):
    try:
        if os.path.exists(directory):
            if os.listdir(directory):
                logger.debug(f"Directory exists and is not empty: {directory}")
                create_backup(directory)
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                logger.debug(f"Contents of {directory} deleted")
            else:
                logger.debug(f"Directory exists but is empty: {directory}")
        else:
            os.makedirs(directory)
            logger.debug(f"Directory created: {directory}")
    except Exception as e:
        logger.exception("Could not access directory. Is the drive still locked?")
        logger.exception(f"Error: {e}")
        time.sleep(5)
        exit()

def copy_audio_files(src, target):
    try:
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.endswith(file_extensions):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(target, file)
                    try:
                        if os.path.exists(destination_path):
                            if files_are_identical(source_path, destination_path):
                                logger.debug(f"Skipped (identical): {source_path} -> {destination_path}")
                                continue  # Skip identical file
                        shutil.copy(source_path, destination_path)
                        logger.debug(f"Copied: {source_path} -> {destination_path}")
                    except Exception as e:
                        logger.exception(f"Error copying file {file}. Reason: {e}")
                        raise
    except Exception as e:
        logger.exception(f"An error occurred during the copy process: {e}")
        raise

def main():
    try:
        create_directory(target_dir)
        copy_audio_files(source_dir, target_dir)
        logger.debug("Copy operation finished.")
    except Exception as e:
        logger.exception(f'Error during copy operation: {e}')
        logger.exception('Restoring original state from backup...')
        restore_backup_for_target(target_dir)
        logger.exception('Restore completed.')

if __name__ == "__main__":
    main()
