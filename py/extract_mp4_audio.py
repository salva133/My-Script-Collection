import os
import subprocess
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_audio_from_mp4():
    """
    Extracts audio from all MP4 files in the current working directory
    and saves them as MP3 files with the same name.
    """
    cwd = os.getcwd()
    logger.info(f"Scanning directory: {cwd}")
    
    for file in os.listdir(cwd):
        if file.lower().endswith(".mp4"):
            mp4_path = os.path.join(cwd, file)
            mp3_path = os.path.splitext(mp4_path)[0] + ".mp3"
            
            logger.info(f"Processing file: {file}")
            
            command = [
                "ffmpeg", "-i", mp4_path, "-c:a", "copy", "-map", "a", mp3_path, "-y"
            ]
            
            try:
                subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
                logger.info(f"Extracted: {mp3_path}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to extract audio from {file}: {e.stderr.decode().strip()}")
            except Exception as e:
                logger.error(f"Unexpected error processing {file}: {e}")

if __name__ == "__main__":
    extract_audio_from_mp4()
