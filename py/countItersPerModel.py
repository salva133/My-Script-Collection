"""
Script Name: countItersPerModel.py
Description: This script processes text files in a specific directory, extracting the current iteration number 
             from each file, and then outputs a summary file with cleaned file names and their corresponding 
             iteration numbers. The summary is sorted in descending order by iteration number.

Functions:
    get_files(directory, extension, prefix) - Retrieves all files in the given directory with specified extension and prefix.
    extract_iterations(file_path) - Extracts the current iteration number from the file.
    clean_file_names(file_names, substring) - Removes a specified substring from a list of file names.
    format_and_write_data(file_info_list, output_file, max_length) - Formats the extracted data and writes it to a new file.
    main() - Main function to orchestrate the process.
"""

import os
import re

def get_files(directory, extension, prefix):
    """Retrieve all files in the given directory with specified extension and prefix."""
    return [filename for filename in os.listdir(directory) 
            if filename.endswith(extension) and not filename.startswith(prefix)]

def extract_iterations(file_path):
    """Extract current iteration number from the file."""
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'current iteration:\s+(\d+)', line, re.IGNORECASE)
            if match:
                return int(match.group(1))
    return None

def clean_file_names(file_names, substring):
    """Remove a specified substring from a list of file names."""
    return [name.replace(substring, '') for name in file_names]

def format_and_write_data(file_info_list, output_file, max_length):
    """Format the extracted data and write it to a new file."""
    with open(output_file, 'w') as summary_file:
        for original_name, iterations in file_info_list:
            cleaned_name = original_name.replace('_SAEHD_summary.txt', '')
            space_count = max_length - len(cleaned_name) + 2
            summary_file.write(f'{cleaned_name}{" " * space_count}: {iterations}\n')

def main():
    directory = './P_RTM Training/workspace/model'
    output_file = 'model_summary_results.txt'
    file_info_list = []

    for filename in get_files(directory, "_summary.txt", "XSeg"):
        iterations = extract_iterations(os.path.join(directory, filename))
        if iterations is not None:
            file_info_list.append((filename, iterations))

    file_info_list.sort(key=lambda x: x[1], reverse=True)
    max_name_length = max(len(name) for name, _ in file_info_list)
    cleaned_file_names = clean_file_names([name for name, _ in file_info_list], '_SAEHD_summary.txt')

    format_and_write_data(file_info_list, output_file, max_name_length)

if __name__ == "__main__":
    main()
