"""
Script Name: countItersPerModel.py
Description: This script processes text files within a specified directory, extracts the iteration counts from each file, and outputs a summary file. The entries in the summary file are grouped by iteration milestones (100k steps) and formatted for uniform spacing, ensuring that the colon appears at the 28th position on each line, and the iteration count starts three characters after the colon. The names are truncated after the first underscore.

Functions:
    get_files(directory, extension, prefix): Retrieves all files in the specified directory with the given extension and prefix.
    extract_iterations(file_path): Extracts the current iteration number from the file.
    clean_file_names(file_names, substring): Removes a specified substring from a list of file names.
    format_and_write_grouped_data(file_info_list, output_file): Groups and formats the extracted data, then writes it to a new file.
    main(): Orchestrates the process flow from data extraction to file output.
"""

import os
import re

def get_files(directory, extension, prefix):
    """Retrieves all files in the specified directory with the given extension and prefix."""
    return [filename for filename in os.listdir(directory)
            if filename.endswith(extension) and not filename.startswith(prefix)]

def extract_iterations(file_path):
    """Extracts the current iteration number from the file."""
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'current iteration:\s+(\d+)', line, re.IGNORECASE)
            if match:
                return int(match.group(1))
    return None

def clean_file_names(file_names, substring):
    """Removes a specified substring from a list of file names."""
    return [name.replace(substring, '') for name in file_names]

def format_and_write_grouped_data(file_info_list, output_file):
    """Groups and formats the extracted data, then writes it to a new file."""
    grouped_data = {}
    for original_name, iterations in file_info_list:
        short_name = original_name.split('_')[0]
        
        if iterations < 100000:
            group = "<100k"
        else:
            group = f"{(iterations // 100000) * 100}k"
        
        if group not in grouped_data:
            grouped_data[group] = []
        grouped_data[group].append((short_name, iterations))
    
    with open(output_file, 'w') as summary_file:
        for group in sorted(grouped_data.keys(), key=lambda x: int(x[:-1]) if x != "<100k" else 0, reverse=True):
            summary_file.write(f"\n### {group} ###\n")
            for name, iter_count in sorted(grouped_data[group], key=lambda x: x[1], reverse=True):
                name_formatted = f"{name.ljust(24)}: "
                iteration_str = f"{iter_count}".rjust(3)
                summary_file.write(f"{name_formatted}{iteration_str}\n")

def main():
    """Orchestrates the process flow from data extraction to file output."""
    directory = './P_RTM Training/workspace/model'
    output_file = 'model_summary_results.txt'
    file_info_list = []

    for filename in get_files(directory, "_summary.txt", "XSeg"):
        iterations = extract_iterations(os.path.join(directory, filename))
        if iterations is not None:
            file_info_list.append((filename, iterations))

    format_and_write_grouped_data(file_info_list, output_file)

if __name__ == "__main__":
    main()