import os
import subprocess

def extract_audio_from_mp4():
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.lower().endswith(".mp4"):
            mp4_path = os.path.join(cwd, file)
            mp3_path = os.path.splitext(mp4_path)[0] + ".mp3"
            
            command = [
                "ffmpeg", "-i", mp4_path, "-c:a", "copy", "-map", "a", mp3_path, "-y"
            ]
            
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Extracted: {mp3_path}")

if __name__ == "__main__":
    extract_audio_from_mp4()
