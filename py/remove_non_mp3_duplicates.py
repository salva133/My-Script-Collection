import os
import re

def find_redundant_files(directory):
    file_map = {}
    
    # Regex to match files without extensions
    pattern = re.compile(r"(.+)\.(m4a|mp3|wav|flac|aac|ogg|wma)")
    
    for root, _, files in os.walk(directory):
        for file in files:
            match = pattern.match(file)
            if match:
                base_name, ext = match.groups()
                if base_name not in file_map:
                    file_map[base_name] = []
                file_map[base_name].append((ext, os.path.join(root, file)))
    
    return file_map

def move_non_mp3_duplicates():
    directory = os.getcwd()
    file_map = find_redundant_files(directory)
    tbd_folder = os.path.join(directory, "TBD")
    
    # Ensure TBD folder exists and clear it if not empty
    if os.path.exists(tbd_folder):
        for file in os.listdir(tbd_folder):
            file_path = os.path.join(tbd_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(tbd_folder)
    
    for base_name, files in file_map.items():
        formats = {ext: path for ext, path in files}
        
        # If multiple formats exist, prefer keeping mp3 and move others
        if 'mp3' in formats:
            for ext, path in formats.items():
                if ext != 'mp3':
                    print(f"Moving: {path} to {tbd_folder}")
                    os.rename(path, os.path.join(tbd_folder, os.path.basename(path)))

def main():
    move_non_mp3_duplicates()
    print("Non-MP3 redundant files moved to TBD folder successfully.")

if __name__ == "__main__":
    main()
