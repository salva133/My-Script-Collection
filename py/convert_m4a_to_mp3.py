import os
import logging
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
import shutil

# Mapping of M4A keys to ID3 keys
metadata_map = {
    '©nam': 'title',
    '©ART': 'artist',
    '©alb': 'album',
    'aART': 'albumartist',
    '©gen': 'genre',
    'trkn': 'tracknumber',
}

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("conversion.log"),  # Log to a file named 'conversion.log'
        logging.StreamHandler()  # Also log to the console
    ]
)

def convert_m4a_to_mp3(directory):
    processed_folder = os.path.join(directory, "_processed")
    
    # Create _processed folder if it doesn't exist
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
        logging.info(f"Created _processed folder at {processed_folder}")

    # Go through all files in the current directory
    for filename in os.listdir(directory):
        if filename.endswith(".m4a"):
            m4a_path = os.path.join(directory, filename)
            mp3_filename = filename.replace(".m4a", ".mp3")
            mp3_path = os.path.join(directory, mp3_filename)
            
            logging.info(f"Processing file: {filename}")
            
            # Extract metadata from the .m4a file
            try:
                m4a_audio = MP4(m4a_path)
                metadata = {}
                for key, value in m4a_audio.tags.items():
                    if key in metadata_map:
                        # If value is a list, grab the first item
                        metadata_value = value[0] if isinstance(value, list) else value
                        
                        # Special case for tracknumber: convert tuple to string
                        if key == 'trkn' and isinstance(metadata_value, tuple):
                            metadata[metadata_map[key]] = f"{metadata_value[0]}/{metadata_value[1]}"  # e.g., "1/12"
                        else:
                            # Ensure value is a string
                            metadata[metadata_map[key]] = str(metadata_value)
                logging.info(f"Extracted metadata for {filename}: {metadata}")
            except Exception as e:
                logging.error(f"Error reading metadata from {filename}: {e}")
                metadata = {}

            # Convert m4a to mp3, replace if mp3 already exists
            try:
                audio = AudioSegment.from_file(m4a_path, format="m4a")
                audio.export(mp3_path, format="mp3")
                logging.info(f"Converted {filename} to {mp3_filename}")
            except Exception as e:
                logging.error(f"Error converting {filename}: {e}")
                continue

            # Apply metadata to the mp3 file
            try:
                mp3_audio = EasyID3(mp3_path)
                for key, value in metadata.items():
                    if value:
                        mp3_audio[key] = value  # Metadata must be strings
                mp3_audio.save()
                logging.info(f"Metadata applied to {mp3_filename}")
            except Exception as e:
                logging.error(f"Error applying metadata to {filename}: {e}")

            # Move the processed .m4a file to the _processed folder
            try:
                processed_m4a_path = os.path.join(processed_folder, filename)
                shutil.move(m4a_path, processed_m4a_path)
                logging.info(f"Moved {filename} to _processed folder")
            except Exception as e:
                logging.error(f"Error moving {filename} to _processed: {e}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    logging.info(f"Starting conversion in directory: {current_directory}")
    convert_m4a_to_mp3(current_directory)
    logging.info("Conversion process completed.")
