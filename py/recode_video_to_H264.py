import os
import subprocess

def scan_videos(cwd):
    video_files = []
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file.endswith(('.mp4', '.mkv', '.avi')):
                video_files.append(os.path.join(root, file))
    return video_files

def check_codec(video_file):
    try:
        result = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                          '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1',
                                          video_file])
        codec = result.decode('utf-8').strip()
        return codec != 'h264'
    except subprocess.CalledProcessError:
        return False

def recode_video(video_file):
    base, ext = os.path.splitext(video_file)
    output_file = f"{base}_recodedH264{ext}"
    try:
        subprocess.run(['ffmpeg', '-i', video_file, '-c:v', 'libx264', '-crf', '23', '-c:a', 'copy', output_file], check=True)
        print(f"Video erfolgreich rekodiert: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Rekodieren von {video_file}: {e}")

if __name__ == "__main__":
    cwd = os.getcwd()
    video_files = scan_videos(cwd)
    non_h264_videos = [file for file in video_files if check_codec(file)]
    
    if non_h264_videos:
        print("Videos, die nicht mit H.264 codiert sind:")
        for i, video in enumerate(non_h264_videos, 1):
            print(f"{i}. {video}")
        
        selection = input("Wähle ein Video zum Rekodieren (Nummer): ")
        try:
            selection = int(selection) - 1
            if 0 <= selection < len(non_h264_videos):
                recode_video(non_h264_videos[selection])
            else:
                print("Ungültige Auswahl.")
        except ValueError:
            print("Bitte eine Zahl eingeben.")
    else:
        print("Keine Videos gefunden, die nicht mit H.264 codiert sind.")
