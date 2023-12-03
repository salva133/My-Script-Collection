import os
import sys
import time

def get_project_name():
    """
    Asks the user for a project name and returns the project name
    with the first letter after each space capitalized and spaces removed.
    """
    project_name = input("Enter a project name: ")
    project_name = "".join(word.capitalize() for word in project_name.split())
    return project_name

def create_directory(directory_name):
    """
    Creates a directory with the given directory name if it doesn't already exist.
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Created directory: {directory_name}")
    else:
        print(f"Directory '{directory_name}' already exists.")

def create_subdirectories(parent_directory, subdirectories):
    """
    Creates subdirectories inside the given parent directory.
    """
    for subdirectory in subdirectories:
        path = os.path.join(parent_directory, subdirectory)
        create_directory(path)

def create_project_structure(project_name):
    """
    Creates the project structure including the main project directory
    and its subdirectories 'media', 'rendered', and 'media/rec'.
    """
    print("Creating project structure...")
    time.sleep(1)

    # Create the main project directory
    create_directory(project_name)

    # Create subdirectories
    subdirectories = ["media", "rendered"]
    create_subdirectories(project_name, subdirectories)

    # Create subdirectories within the media and rendered directories
    media_rendered_subdirectories = ["thumbnail"]
    create_subdirectories(os.path.join(project_name, "media"), media_rendered_subdirectories)
    create_subdirectories(os.path.join(project_name, "rendered"), media_rendered_subdirectories)

    # Create subdirectory within the media directory
    create_directory(os.path.join(project_name, "media", "rec"))

    print("Project structure created successfully.")

def main():
    # Get the formatted project name
    project_name = get_project_name()

    # Create the project structure
    create_project_structure(project_name)

    # Wait for 10 seconds before the program exits
    print("Waiting for 1 seconds before exit...")
    time.sleep(1)

def write_error_log(error_message):
    """
    Writes the given error message to a log file with the format <script_file_name>_error.log.
    """
    script_name = os.path.basename(sys.argv[0])
    log_file_name = f"{os.path.splitext(script_name)[0]}_error.log"

    with open(log_file_name, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        write_error_log(error_message)
