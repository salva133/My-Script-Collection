"""
Script Name: convert_audio_to_wav.py
Description: This script converts audio files from various formats to WAV format. It searches for audio files within a specified input directory, supports multiple source formats, and places the converted WAV files into an output directory. The script uses FFmpeg for the conversion process.

Functions:
    convert_to_wav(input_directory, output_directory="converted_audio") - Converts all supported audio formats found in the input directory to WAV format, storing them in the output directory.

Workflow:
    1. Check for the existence of the output directory and create it if necessary.
    2. Search for audio files of specified formats within the input directory.
    3. Convert each found audio file to WAV format using FFmpeg, maintaining standard audio quality settings.
"""

import subprocess
import os
import glob

def convert_to_wav(input_directory, output_directory="converted_audio"):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Sucht nach gängigen Audioformaten im angegebenen Verzeichnis
    audio_formats = ["*.mp3", "*.ogg", "*.flac", "*.aac", "*.m4a", "*.wav"]
    files_to_convert = []
    for format in audio_formats:
        pattern = os.path.join(input_directory, format)
        found_files = glob.glob(pattern)
        files_to_convert.extend(found_files)
        print(f"Gefundene Dateien für Format {format}: {found_files}")

    for file in files_to_convert:
        filename = os.path.basename(file)
        output_file = os.path.join(output_directory, os.path.splitext(filename)[0] + '.wav')
        subprocess.run(["ffmpeg", "-i", file, "-ar", "44100", "-ac", "2", output_file], check=True)
        print(f"Konvertiert: {file} -> {output_file}")

# Aktuelles Verzeichnis als Eingabeverzeichnis
input_directory = os.getcwd()
convert_to_wav(input_directory)
