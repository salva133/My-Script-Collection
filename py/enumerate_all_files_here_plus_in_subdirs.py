import os
from pathlib import Path
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import logging
# from create_manifest import create_manifest

FORCE_CHANGE = False  # Global variable to force renaming and metadata update regardless of current state
ARTIST = "Witch Doctor Larry"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def remove_existing_number(file_name):
    """
    Removes a leading number and underscore from a file name (e.g., '001_filename' becomes 'filename').
    """
    try:
        pattern = r'^\d+_'
        logger.debug(f"Removing number from {file_name}")
        return re.sub(pattern, '', file_name)
    except Exception as e:
        logger.exception(f"Error removing number from {file_name}: {e}")
        return file_name

def extract_track_info(file_name):
    """
    Extracts track number and title from a file name formatted as '001_filename.ext'.
    Returns both the track number and the title without the extension.
    """
    try:
        logger.debug(f"Extracting track info from {file_name}")
        match = re.match(r'^(\d+)_', file_name)
        if match:
            track_number = match.group(1)
            title = remove_existing_number(file_name).rsplit('.', 1)[0]
            return track_number, title
        return None, None
    except Exception as e:
        logger.exception(f"Error extracting track info from {file_name}: {e}")
        return None, None

def is_valid_audio_file(file):
    """
    Checks if the file is an audio file based on its extension (e.g., .mp3, .wav, .flac, .aac).
    Returns True if it is an audio file, False otherwise.
    """
    try:
        logger.debug(f"Checking if {file} is a valid audio file")
        audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.m4a'}
        return file.suffix.lower() in audio_extensions
    except Exception as e:
        logger.exception(f"Error checking if file is a valid audio file: {e}")
        return False

def get_files_to_rename(directory: Path):
    """
    Iterates through a directory and returns a list of files that are audio files.
    """
    try:
        logger.info(f"Scanning directory {directory} for audio files to rename")
        return [f for f in directory.iterdir() if f.is_file() and is_valid_audio_file(f)]
    except Exception as e:
        logger.exception(f"Error iterating directory {directory}: {e}")
        return []

def rename_files_in_directory(directory: Path):
    """
    Processes all files in the directory, renames them, and updates metadata for audio files.
    """
    logger.info(f"Starting processing of directory: {directory}")
    files = get_files_to_rename(directory)
    cleaned_files = [(file, remove_existing_number(file.name)) for file in files]
    cleaned_files.sort(key=lambda x: x[0].stat().st_ctime, reverse=True)
    
    num_digits = len(str(len(cleaned_files)))
    
    for i, (file, clean_name) in enumerate(cleaned_files, start=1):
        try:
            new_name = f"{i:0{num_digits}d}_{clean_name}"
            logger.debug(f"Preparing to rename {file.name} to {new_name}")
            
            if not FORCE_CHANGE and new_name == file.name:
                logger.debug(f"Skipping renaming for {file.name}: No change required.")
                add_metadata(file, directory.name)
                continue
            
            new_path = directory / new_name
            logger.debug(f"Renaming: {file.name} -> {new_name}")
            file.rename(new_path)
            add_metadata(new_path, directory.name)
        except Exception as e:
            logger.exception(f"Error renaming {file.name} to {new_name}: {e}")

def add_metadata(file, album_name):
    """
    Adds metadata to an audio file but saves only if something changes.
    """
    try:
        try:
            audio = EasyID3(file)
        except ID3NoHeaderError:
            audio = EasyID3()
        
        track_number, title = extract_track_info(file.name)
        if not track_number or not title:
            return  # If no track information can be extracted, do nothing

        existing_metadata = {
            "tracknumber": audio.get("tracknumber", [None])[0],
            "title": audio.get("title", [None])[0],
            "artist": audio.get("artist", [None])[0],
            "album": audio.get("album", [None])[0],
        }

        new_metadata = {
            "tracknumber": track_number,
            "title": title,
            "artist": ARTIST,
            "album": album_name,
        }

        if existing_metadata == new_metadata:
            logger.debug(f"Metadata unchanged for {file}, save skipped.")
            return

        audio["tracknumber"] = track_number
        audio["title"] = title
        audio["artist"] = ARTIST
        audio["album"] = album_name
        audio.save(file)
        logger.debug(f"Metadata saved for {file}")
    except Exception as e:
        logger.exception(f"Error adding metadata to {file}: {e}")

def process_directory(directory: Path):
    """
    Recursively processes a directory and all its subdirectories by renaming files and updating their metadata.
    """
    try:
        rename_files_in_directory(directory)
    except Exception as e:
        logger.exception(f"Error processing directory {directory}: {e}")
    
    for subdir in directory.iterdir():
        if subdir.is_dir():
            try:
                process_directory(subdir)
            except Exception as e:
                logger.exception(f"Error processing subdirectory {subdir}: {e}")
                
def main():
    try:
        cwd = Path(os.getcwd())
        logger.info(f"Starting processing in directory: {cwd}")
        process_directory(cwd)
        # create_manifest()
    except Exception as e:
        logger.exception(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
