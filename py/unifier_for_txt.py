import os

def debug_print(message):
    """Print debug messages to track the script execution."""
    print(f"[DEBUG] {message}")

def read_file(file_path):
    debug_print(f"Reading file: {file_path}")
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1']  # Liste der zu verwendenden Encodings
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                debug_print(f"Successfully read file with encoding: {encoding}")
                return file.read()
        except UnicodeDecodeError:
            debug_print(f"Failed to read file with encoding: {encoding}")
            continue
    debug_print(f"Failed to read file: {file_path} with any known encoding")
    return None

def combine_txt_files(output_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Verzeichnis des Skripts
    debug_print(f"Script directory: {script_dir}")
    debug_print(f"Output file: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        debug_print(f"Opened output file: {output_file}")
        for root, dirs, files in os.walk(script_dir):
            debug_print(f"Walking directory: {root}")
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    debug_print(f"Processing file: {file_path}")
                    content = read_file(file_path)
                    if content:
                        outfile.write(content)
                        outfile.write('\n')  # Optional: Fügt eine neue Zeile zwischen Dateien hinzu
                        debug_print(f"Wrote content of file: {file_path} to output file")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Verzeichnis des Skripts
    output_file = os.path.join(script_dir, 'combined.txt')  # Ausgabedatei im Skriptverzeichnis
    debug_print("Starting file combination process")
    combine_txt_files(output_file)
    debug_print(f'All .txt files have been combined into {output_file}')
