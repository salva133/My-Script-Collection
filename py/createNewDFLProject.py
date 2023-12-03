import os
import shutil
from tqdm import tqdm

DEBUG_MODE = False

def get_new_folder_name():
    return input("Enter the desired folder name: ")
    
def select_folder_from_aligned():
    base_path = ".\\P_RTM Training\\workspace\\data_src\\aligned"
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")
    
    choice = int(input("Select a folder by number: "))
    return os.path.join(base_path, folders[choice - 1])

def copy_faceset_to_new_folder(selected_folder, target_folder):
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
    for file in os.listdir(folder_path):
        if file.startswith("_"):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    print("Cleanup complete.")

def calculate_total_size(source_folder_path):
    return sum(os.path.getsize(os.path.join(path, file)) for path, _, files in os.walk(source_folder_path) for file in files)

def copy_files_with_progress(source_folder_path, copied_folder, total_size):
    progress_bar = tqdm(total=total_size, unit="B", desc="Copying files", unit_scale=True)
    for root, _, files in os.walk(source_folder_path):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(copied_folder, os.path.relpath(root, source_folder_path), file)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            progress_bar.update(os.path.getsize(src_path))
    progress_bar.close()

def copy_and_rename_folder(source_folder, new_folder_name, selected_folder):
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

    total_size = calculate_total_size(source_folder_path)
    copy_files_with_progress(source_folder_path, copied_folder, total_size)
    delete_files_starting_with_underscore(copied_folder)

    print(f"The folder '{source_folder}' has been copied and renamed to '{new_folder_name}'.")

def main():
    if DEBUG_MODE:    
        print("Starting execution...")
    
    new_folder_name = get_new_folder_name()
    selected_folder = select_folder_from_aligned()
    copy_and_rename_folder("_rebuild", new_folder_name, selected_folder)
    
    if DEBUG_MODE:
        print("Execution complete. End of Program.")

if __name__ == "__main__":
    main()
