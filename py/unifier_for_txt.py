import os

def read_file(file_path):
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1']  # List of encodings to try
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    return None

def combine_txt_files(output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    content = read_file(file_path)
                    if content:
                        outfile.write(content)
                        outfile.write('\n')  # Optional: Adds a newline between files

if __name__ == "__main__":
    output_file = 'combined.txt'
    combine_txt_files(output_file)
    print(f'All .txt files have been combined into {output_file}')
