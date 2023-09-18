import os
from pathlib import Path
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import logging

FORCE_CHANGE = False  # Global variable to force renaming and metadata update regardless of current state

logging.basicConfig(level=logging.INFO, # Logger Config
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def remove_existing_number(file_name):
    """
    Removes a leading number and underscore from a file name (e.g., '001_filename' becomes 'filename').
    """
    try:
        pattern = r'^\d+_'
        logger.debug(f"Entferne Nummer aus {file_name}")
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
        logger.debug(f"Extrahiere Track-Informationen aus {file_name}")
        match = re.match(r'^(\d+)_', file_name)
        if match:
            track_number = match.group(1)
            title = remove_existing_number(file_name).rsplit('.', 1)[0]
            return track_number, title
        return None, None
    except Exception as e:
        logger.exception(f"Error extracting track info from {file_name}: {e}")
        return None, None

def is_invalid_file(file):
    """
    Checks if the file is a script or an image file that should be ignored for renaming.
    Returns True if the file should be skipped, False otherwise.
    """
    try:
        logger.debug(f"Überprüfe, ob {file} ein ungültiges Dateiformat ist")
        file_extensions = {'.py', '.sh', '.bat', '.cmd', '.pl', '.rb', '.js', '.png', '.jpg', '.bmp', '.ini'}
        return file.suffix in file_extensions
    
    except Exception as e:
        logger.exception(f"Error checking if file is a script: {e}")
        return False

def is_audio_file(file):
    """
    Checks if the file is an audio file based on its extension (e.g., .mp3, .wav, .flac, .aac).
    Returns True if it is an audio file, False otherwise.
    """
    try:
        logger.debug(f"Überprüfe, ob {file} eine Audiodatei ist")
        audio_extensions = {'.mp3', '.wav', '.flac', '.aac'}
        return file.suffix.lower() in audio_extensions
    except Exception as e:
        logger.exception(f"Error checking if file is audio: {e}")
        return False

def get_files_to_rename(directory: Path):
    """
    Iterates through a directory and returns a list of files that are not scripts or image files.
    """
    try:
        logger.info(f"Scanne Verzeichnis {directory} nach Dateien zum Umbenennen")
        return [f for f in directory.iterdir() if f.is_file() and not is_invalid_file(f)]
    
    except Exception as e:
        logger.exception(f"Error iterating directory {directory}: {e}")
        return []

def clean_file_names(files):
    """
    Removes leading numbers and underscores from the names of all files in the list.
    Returns a list of tuples containing the original file and the cleaned name.
    """
    try:
        logger.info(f"Reinige Dateinamen von {len(files)} Dateien")
        return [(file, remove_existing_number(file.name)) for file in files]
   
    except Exception as e:
        logger.exception(f"Error cleaning file names: {e}")
        return files

def sort_files_by_creation_time(cleaned_files):
    """
    Sorts files by their creation time in descending order.
    """
    try:
        logger.debug("Sortiere Dateien nach Erstellungszeit")
        cleaned_files.sort(key=lambda x: x[0].stat().st_ctime, reverse=True)
        return cleaned_files
    
    except Exception as e:
        logger.exception(f"Error sorting files by creation time: {e}")
        return cleaned_files

def rename_files(cleaned_files, directory: Path):
    """
    Renames files by adding a numbered prefix (e.g., '001_filename'). If FORCE_CHANGE is True, 
    forces renaming and metadata update even if the name or metadata is already correct.
    """
    num_digits = len(str(len(cleaned_files)))
    
    for i, (file, clean_name) in enumerate(cleaned_files, start=1):
        try:
            new_name = f"{i:0{num_digits}d}_{clean_name}"
            logger.debug(f"Bereite Umbenennung von {file.name} zu {new_name} vor")
            
            if not FORCE_CHANGE and new_name == file.name:
                logger.debug(f"Überspringe Umbenennung für {file.name}: Keine Änderung erforderlich.")
                if is_audio_file(file):
                    add_metadata(file, directory.name)
                continue
            
            new_path = directory / new_name
            logger.info(f"Umbenennen: {file.name} -> {new_name}")
            file.rename(new_path)
            
            if is_audio_file(new_path) or FORCE_CHANGE:
                add_metadata(new_path, directory.name)
        
        except Exception as e:
            logger.exception(f"Fehler beim Umbenennen von {file.name} zu {new_name}: {e}")

def add_metadata(file, album_name):
    """
    Adds metadata to an audio file using the EasyID3 tag system. The metadata includes 
    track number, title, artist, and album information extracted from the file name and the directory name.
    """
    try:
        try:
            audio = EasyID3(file)
        except ID3NoHeaderError:
            audio = EasyID3()

        track_number, title = extract_track_info(file.name)

        if track_number and title:
            audio['tracknumber'] = track_number
            audio['title'] = title
        audio['artist'] = "Witch Doctor Larry"
        audio['album'] = album_name
        audio.save(file)
        logger.debug(f"Metadaten zu {file} hinzugefügt: Track = {track_number}, Title = '{title}', Artist = 'Witch Doctor Larry', Album = '{album_name}'")
    
    except Exception as e:
        logger.exception(f"Error adding metadata to {file}: {e}")

def rename_files_in_directory(directory: Path):
    """
    Processes all files in the directory, renames them, and updates metadata for audio files.
    """
    logger.info(f"Beginne Verarbeitung des Verzeichnisses: {directory}")
    files = get_files_to_rename(directory)
    cleaned_files = clean_file_names(files)
    sorted_files = sort_files_by_creation_time(cleaned_files)
    rename_files(sorted_files, directory)

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

if __name__ == "__main__":
    """
    Entry point of the script. Begins processing from the current working directory.
    """
    try:
        cwd = Path(os.getcwd())
        logger.info(f"Starte Verarbeitungsprozess im Verzeichnis: {cwd}")
        process_directory(cwd)
        # input("Umbenennung abgeschlossen.")
        
    except Exception as e:
        logger.exception(f"Error in main execution: {e}")
