import os
from pydub import AudioSegment

def convert_to_ogg(file_path):
    audio = AudioSegment.from_file(file_path)
    ogg_file_path = os.path.splitext(file_path)[0] + ".ogg"
    audio.export(ogg_file_path, format="ogg")
    print(f"Convert: {file_path} -> {ogg_file_path}")

def convert_all_audio_to_ogg():
    supported_formats = (".mp3", ".wav", ".flac", ".aac", ".m4a", ".wma")
    cwd = os.getcwd()
    
    for file_name in os.listdir(cwd):
        if file_name.endswith(supported_formats):
            file_path = os.path.join(cwd, file_name)
            convert_to_ogg(file_path)

if __name__ == "__main__":
    convert_all_audio_to_ogg()
