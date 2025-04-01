import os
import re

# Pattern for allowed characters (alphanumeric characters, underscore, dot, and space)
pattern = re.compile(r'[^a-zA-Z0-9_. ]')
paren_pattern = re.compile(r'\s*\((\d+kbit_[A-Z]+)\)\s*')  # Removes only brackets with bitrate and codec info

def replace_umlauts(text):
    umlaut_map = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'
    }
    for umlaut, replacement in umlaut_map.items():
        text = text.replace(umlaut, replacement)
    return text

def process_filename(filename):
    # Teile den Dateinamen in Basisname und Endung
    name, ext = os.path.splitext(filename)
    
    # Ersetze Umlaute im Basisnamen
    name = replace_umlauts(name)

    # Entferne Substrings, die dem Muster (.*p_.*fps_.*-.*kbit_.*) entsprechen
    name = re.sub(r'\(.*p_.*fps_.*-.*kbit_.*?\)', '', name)

    # Entferne weitere spezifizierte Klammerinhalte
    name = re.sub(paren_pattern, '', name)

    # Entferne unerwünschte Sonderzeichen sowie "4K" und "ASMR", normalisiere Leerzeichen und trimme
    cleaned = re.sub(r'\s+', ' ',
                     pattern.sub('', name.replace("4K", "").replace("ASMR", ""))
                     ).strip()

    # Füge Leerzeichen zwischen Kleinbuchstaben und direkt folgendem Großbuchstaben ein (CamelCase)
    cleaned = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', cleaned)

    # Letztes Trimming, um restliche Leerzeichen zu entfernen
    cleaned = cleaned.strip()
    
    # Füge den bereinigten Basisnamen mit der originalen Endung (ebenfalls getrimmt) zusammen
    return cleaned + ext.strip()

def rename_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Process the filename
            new_filename = process_filename(filename)
            
            # Full path to the files
            old_file_path = os.path.join(root, filename)
            new_file_path = os.path.join(root, new_filename)
            
            # Rename the file if the new name is different
            if new_filename != filename:
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")

def main():
    # Start the process in the current directory (including subdirectories)
    try:
        cwd = os.getcwd()
        rename_files_in_directory(cwd)
        print("Done!")
    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    #     input("Program finished.")

if __name__ == "__main__":
    main()
