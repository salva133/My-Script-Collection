import os
import shutil


def main():
    try:
        # Get parent directory and check if the current directory is valid
        parent_dir = get_parent_directory()
        check_current_directory()

        # Print synchronization warning and list affected folders
        print_sync_warning()
        affected_folders = get_affected_folders(parent_dir)
        print_affected_folders(affected_folders)

        # Prompt user to continue or cancel the synchronization process
        user_input = input("\nDo you want to continue? (y/n) ")
        if user_input.lower() == "y":
            sync_scripts(parent_dir, affected_folders)
        else:
            print("The process has been canceled.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_parent_directory():
    # Get the absolute path of the parent directory
    return os.path.abspath(os.path.join(os.getcwd(), os.pardir))


def check_current_directory():
    # Check if the script is running in the '_rebuild' folder
    if os.path.basename(os.getcwd()) != "_rebuild":
        raise Exception("This script can only be executed in the _rebuild folder.")


def print_sync_warning():
    # Print a warning message about the synchronization process
    print("Starting script synchronization...\nWARNING: This process will delete all existing .bat and .py files in all project directories and replace them with the ones currently in _rebuild. This process is irreversible.")


def get_affected_folders(parent_dir):
    # Get a list of affected folders (directories starting with 'V_', or 'F_')
    return [dir_name for dir_name in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, dir_name)) and dir_name != os.path.basename(os.getcwd()) and dir_name.startswith(("V_", "F_"))]


def print_affected_folders(affected_folders):
    # Print the list of affected folders
    print("\nThe following folders will be affected by this process:")
    for folder in affected_folders:
        print(folder)


def sync_scripts(parent_dir, affected_folders):
    # Synchronize scripts for all affected folders
    for dir_name in affected_folders:
        try:
            remove_old_scripts(parent_dir, dir_name)
            copy_new_scripts(parent_dir, dir_name)
            print(f"Successfully processed folder {dir_name}")
        except Exception as e:
            print(f"An error occurred while processing folder {dir_name}: {e}")


def remove_old_scripts(parent_dir, dir_name):
    # Remove existing .bat and .py files in the target folder
    for file_name in os.listdir(os.path.join(parent_dir, dir_name)):
        if file_name.endswith((".bat", ".py")):
            os.remove(os.path.join(parent_dir, dir_name, file_name))


def copy_new_scripts(parent_dir, dir_name):
    # Copy .bat and .py files from the '_rebuild' folder to the target folder
    for file_name in os.listdir(os.getcwd()):
        if file_name.endswith((".bat", ".py")) and not file_name.startswith("_"):
            shutil.copy(os.path.join(os.getcwd(), file_name), os.path.join(parent_dir, dir_name, file_name))


if __name__ == "__main__":
    main()