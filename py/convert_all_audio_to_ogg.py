import os
import subprocess
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

## EXECUTE WITH 3.10

def check_ffmpeg():
    """Prüft, ob ffmpeg installiert ist und im PATH verfügbar ist."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Fehler: ffmpeg ist nicht installiert oder nicht im PATH.")
        print("Installiere es von: https://ffmpeg.org/download.html")
        exit(1)

def convert_to_ogg(file_path):
    """Konvertiert eine Audiodatei ins OGG-Format mit pydub."""
    try:
        audio = AudioSegment.from_file(file_path)
        ogg_file_path = os.path.splitext(file_path)[0] + ".ogg"
        audio.export(ogg_file_path, format="ogg")
        print(f"Konvertiert: {file_path} -> {ogg_file_path}")
    except CouldntDecodeError:
        print(f"Fehler: Datei {file_path} konnte nicht dekodiert werden.")

def convert_all_audio_to_ogg():
    """Durchsucht das aktuelle Verzeichnis und konvertiert alle unterstützten Audiodateien nach OGG."""
    supported_formats = (".mp3", ".wav", ".flac", ".aac", ".m4a", ".wma")
    cwd = os.getcwd()

    for file_name in os.listdir(cwd):
        if file_name.lower().endswith(supported_formats):
            file_path = os.path.join(cwd, file_name)
            convert_to_ogg(file_path)

def main():
    check_ffmpeg()
    convert_all_audio_to_ogg()

if __name__ == "__main__":
    main()
