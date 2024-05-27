"""
Script Name: mergeFilesIntoAligned.py
Description: This script is designed to consolidate files from multiple subdirectories into a single 'aligned' directory. Before merging, it creates a backup of all files to prevent data loss. The script is particularly useful for organizing dataset files or project assets that are spread across different folders into a unified structure.

Functions:
    create_directory(path) - Creates a new directory if it does not exist.
    backup_files(cwd) - Creates a backup of all files in the current working directory.
    move_files_from_subdirectories(cwd, aligned_dir) - Moves files from all subdirectories into a single specified directory, maintaining a count of total and duplicate files.

Usage:
    1. The script backs up all files in the current working directory to a 'backup' folder.
    2. It then moves all files from each subdirectory into the specified 'aligned' directory.
    3. Duplicate files are noted but not overwritten, ensuring no data is lost during consolidation.
"""


import os
import shutil
from tqdm import tqdm


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def backup_files(cwd):
    backup_dir = create_directory(os.path.join(cwd, "backup"))

    for subdir in os.listdir(cwd):
        subdir_path = os.path.join(cwd, subdir)

        if os.path.isdir(subdir_path):
            for file in os.listdir(subdir_path):
                source = os.path.join(subdir_path, file)
                destination = os.path.join(backup_dir, subdir, file)

                if os.path.isfile(source):
                    os.makedirs(os.path.join(backup_dir, subdir), exist_ok=True)
                    shutil.copy2(source, destination)


def move_files_from_subdirectories(cwd, aligned_dir):
    duplicate_files = []
    total_files = 0
    subdirs = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(cwd, subdir)
        total_files += len(
            [
                f
                for f in os.listdir(subdir_path)
                if os.path.isfile(os.path.join(subdir_path, f))
            ]
        )

    print(f"Es werden {total_files} Dateien aus {len(subdirs)} Ordnern verschoben.")

    for subdir in tqdm(subdirs, desc="Verschieben"):
        subdir_path = os.path.join(cwd, subdir)
        files = os.listdir(subdir_path)

        for file in files:
            source = os.path.join(subdir_path, file)
            destination = os.path.join(aligned_dir, file)

            if os.path.isfile(source):
                if not os.path.exists(destination):
                    shutil.move(source, destination)
                else:
                    duplicate_files.append(file)

    return duplicate_files


def print_duplicate_files(duplicate_files):
    if duplicate_files:
        print("Folgende Dateien wurden aufgrund von Namenskonflikten übersprungen:")
        for duplicate_file in duplicate_files:
            print(duplicate_file)


def remove_empty_directories(cwd):
    for subdir in os.listdir(cwd):
        subdir_path = os.path.join(cwd, subdir)

        if os.path.isdir(subdir_path) and not os.listdir(subdir_path):
            os.rmdir(subdir_path)


def main():
    cwd = os.getcwd()  # Get the current working directory
    aligned_dir = create_directory(
        os.path.join(cwd, "aligned")
    )  # Create the 'aligned' directory
    backup_files(cwd)  # Backup files in the current working directory
    duplicate_files = move_files_from_subdirectories(
        cwd, aligned_dir
    )  # Move files from subdirectories to the 'aligned' directory
    print_duplicate_files(
        duplicate_files
    )  # Print the duplicate files that were skipped due to name conflicts
    remove_empty_directories(
        cwd
    )  # Remove empty directories in the current working directory
    print(
        "Files have been successfully moved to the 'aligned' folder. Empty folders have been deleted."
    )


if __name__ == "__main__":
    main()
