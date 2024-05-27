"""
Script Name: createNewDFLProject.py
Description: This script facilitates the creation of a new DeepFaceLab (DFL) project by automating the process of setting up the necessary folder structure and copying required files. It guides the user through selecting an aligned faceset, naming the new project, and organizing the project's directory structure.

Functions:
    get_new_folder_name() - Prompts the user to enter a desired folder name for the new project.
    select_folder_from_aligned() - Allows user selection of a folder from the 'aligned' directory, based on a substring extracted from the new folder name.
    copy_faceset_to_new_folder() - Copies a faceset file from a selected source to a new project folder, ensuring proper file presence and target directory existence.
    create_subfolder() - Creates a subfolder within a specified directory path after verifying its non-existence.
    format_size() - Converts file size from bytes to a more human-readable format (KB, MB, GB), aiding in file size display.

Table of Contents for Script Functions:

1. get_new_folder_name
   - Prompts the user to enter a desired folder name for the new project.

2. select_folder_from_aligned
   - Allows the user to select a folder from the 'aligned' directory based on a substring extracted from the new folder name.
   - Automatically selects a folder if the extracted substring matches any folder names within the 'aligned' directory.
   - Returns the path to the selected folder and the extracted substring.

3. copy_faceset_to_new_folder
   - Copies a faceset file from a selected source folder to a specified target folder.
   - Ensures the target folder exists and verifies the presence of the faceset file before copying.

4. create_subfolder
   - Creates a subfolder within a specified folder path.
   - Verifies and ensures that the subfolder does not exist before creating it.

5. format_size
   - Converts a file size from bytes to a more readable format (KB, MB, GB).
   - Helps in displaying file sizes in a user-friendly manner.

6. delete_files_starting_with_underscore
   - Deletes files within a specified folder that start with an underscore (_).
   - Typically used for cleanup and preparation of a directory before use in the project.

7. copy_model_files
   - Copies specific model files from the original 'model' directory to a new 'model' directory within the project's workspace.
   - Copies files that either start with a specified substring or start with 'XSeg'.
   - Provides feedback on the files copied and warns if no relevant files were found.

8. copy_and_rename_folder
   - Main function to handle the copying and renaming of a project folder.
   - Utilizes other functions to perform tasks such as copying facesets, creating subfolders, and managing file sizes.
   - Reports the completion of folder copying and renaming.

9. main
   - The main function of the script.
   - Orchestrates the flow of the script by calling other functions in order to set up a new DeepFaceLab project based on user input.

Please note: The main script execution begins by calling the 'main' function if the script is run as the main module.
"""

import os
import shutil
from tqdm import tqdm

DEBUG_MODE = False

def get_new_folder_name():
    return input("Enter the desired folder name: ")
    
def select_folder_from_aligned(new_folder_name):
    print("Opening Selection...")
    base_path = ".\\P_RTM Training\\workspace\\data_src\\aligned"
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

    name_to_search = new_folder_name.split('_', 1)[-1].lower()

    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")
        if name_to_search in folder.lower():
            print(f"Automatically selected '{folder}' based on the entered substring '{new_folder_name}'.")
            return os.path.join(base_path, folders[i - 1]), name_to_search

    choice = int(input("Select a folder by number: "))
    return os.path.join(base_path, folders[choice - 1]), name_to_search

def copy_faceset_to_new_folder(selected_folder, target_folder):
    print("Copying faceset to new folder.")
    print(f"Target folder path: {target_folder}")
    os.makedirs(target_folder, exist_ok=True)
    src_path = os.path.join(selected_folder, "faceset.pak")
    if not os.path.exists(src_path):
        print("Error: faceset.pak not found in selected folder.")
        return
    
    dst_path = os.path.join(target_folder, "faceset.pak")
    shutil.copy2(src_path, dst_path)
    print("'faceset.pak' successfully copied to the target folder.")
    
    shutil.copy2(src_path, target_folder)

def create_subfolder(folder_path, subfolder_name):
    print("Creating Subfolder...")
    subfolder_path = os.path.join(folder_path, subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)
    print(f"Created subfolder '{subfolder_name}' in '{folder_path}'.")

def format_size(n):
    thresholds = [(1024**3, "GB"), (1024**2, "MB"), (1024, "KB")]
    for threshold, unit in thresholds:
        if n >= threshold:
            return f"{int(n/threshold):d} {unit}"
    return f"{n:d} B"

def delete_files_starting_with_underscore(folder_path):
    print("Starting cleanup operation...")
    for file in os.listdir(folder_path):
        if file.startswith("_"):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    print("Cleanup complete.")

def calculate_total_size(source_folder_path):
    if DEBUG_MODE:
        print("Calculating total size...")
    return sum(os.path.getsize(os.path.join(path, file)) for path, _, files in os.walk(source_folder_path) for file in files)

def copy_files_with_progress(source_folder_path, copied_folder, total_size):
    print("Starting copy of rump files.")
    progress_bar = tqdm(total=total_size, unit="B", desc="Copying files", unit_scale=True)
    for root, _, files in os.walk(source_folder_path):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(copied_folder, os.path.relpath(root, source_folder_path), file)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            progress_bar.update(os.path.getsize(src_path))
    progress_bar.close()
    print("Copying rump files completed.")

def copy_and_rename_folder(source_folder, new_folder_name, selected_folder, name_to_search):
    print("Starting copy and renaming of folder")
    if DEBUG_MODE:
        print(f"Used variables: source_folder '{source_folder}', new_folder_name '{new_folder_name}', selected_folder '{selected_folder}', name_to_search '{name_to_search}'")
    cwd = os.getcwd()
    source_folder_path = os.path.join(cwd, source_folder)
    
    if not os.path.exists(source_folder_path):
        print(f"The folder '{source_folder}' could not be found.")
        return

    copied_folder = os.path.join(cwd, new_folder_name)
    if os.path.exists(copied_folder):
        print(f"The folder '{new_folder_name}' already exists. Aborting.")
        return

    os.makedirs(copied_folder)
    create_subfolder(copied_folder, "workspace")
    workspace_folder = os.path.join(copied_folder, "workspace")
    create_subfolder(workspace_folder, "data_src")

    target_folder = os.path.join(workspace_folder, "data_src", "aligned")
    copy_faceset_to_new_folder(selected_folder, target_folder)

    create_subfolder(workspace_folder, "model")
    copy_model_files(name_to_search, workspace_folder)

    total_size = calculate_total_size(source_folder_path)
    copy_files_with_progress(source_folder_path, copied_folder, total_size)
    delete_files_starting_with_underscore(copied_folder)

    print(f"The folder '{source_folder}' has been copied and renamed to '{new_folder_name}'.")
    print("Copy and rename completed.")

def copy_model_files(substring, target_workspace):
    print("Starting copying of model files.")
    model_path = ".\\P_RTM Training\\workspace\\model\\"  
    target_model_path = os.path.join(target_workspace, "model")  
    os.makedirs(target_model_path, exist_ok=True)  

    found_files = False  

    for file in os.listdir(model_path):
        if file.lower().startswith(substring.lower()):
            src_file_path = os.path.join(model_path, file)
            dst_file_path = os.path.join(target_model_path, file)
            shutil.copy2(src_file_path, dst_file_path)
            if DEBUG_MODE:
                print(f"File '{file}' successfully copied to '{target_model_path}'.")
            found_files = True

    for file in os.listdir(model_path):
        if file.startswith("XSeg"):
            src_file_path = os.path.join(model_path, file)
            dst_file_path = os.path.join(target_model_path, file)
            shutil.copy2(src_file_path, dst_file_path)
            if DEBUG_MODE:
                print(f"File '{file}' successfully copied to '{target_model_path}'.")
            found_files = True

    if not found_files:
        print(f"Warning: No files starting with '{substring}' or starting with 'XSeg' were found in the '{model_path}' directory.")
    print("Copying model files finished.")

def main():    
    print("Starting execution...")    
    
    new_folder_name = get_new_folder_name()
    selected_folder, name_to_search = select_folder_from_aligned(new_folder_name) 
    copy_and_rename_folder("_rebuild", new_folder_name, selected_folder, name_to_search)  
    
    print("Execution complete. End of Program.")

if __name__ == "__main__":
    main()
