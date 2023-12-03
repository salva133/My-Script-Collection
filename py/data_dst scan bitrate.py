import os
import cv2

def log_error(message):
    with open('error_log.txt', 'a') as f:
        f.write(message + '\n')

def get_bitrate(file_path):
    try:
        video = cv2.VideoCapture(file_path)
        if not video.isOpened():
            error_message = f"Failed to open {file_path}\n"
            print(error_message)
            log_error(error_message)
            return
        bitrate = video.get(cv2.CAP_PROP_BITRATE) / 1000
        video.release()
        return bitrate
    except Exception as e:
        error_message = f"Error getting bitrate for {file_path}: {e}\n"
        print(error_message)
        log_error(error_message)

def create_bitrate_txt_file(dirpath, bitrate):
    txt_file_path = os.path.join(dirpath, str(bitrate) + 'kbps.txt')
    try:
        with open(txt_file_path, 'w') as f:
            f.write(str(bitrate))
            print(f'Created file: {txt_file_path}\n')
    except Exception as e:
        error_message = f"Failed to write to {txt_file_path}: {e}\n"
        print(error_message)
        log_error(error_message)

def process_directory_with_V_prefix():
    for dir_entry in os.scandir(os.getcwd()):
        if dir_entry.is_dir() and dir_entry.name.startswith('V_'):
            workspace_path = os.path.join(dir_entry.path, 'workspace')
            if os.path.exists(workspace_path):
                process_workspace_directory(workspace_path)

def process_workspace_directory(workspace_path):
    for dirpath, dirnames, filenames in os.walk(workspace_path):
        if 'data_dst.mp4' in filenames:
            file_path = os.path.join(dirpath, 'data_dst.mp4')
            print(f'Found file: {file_path}')
            bitrate = get_bitrate(file_path)
            if bitrate:
                print(f'Bitrate of {file_path}: {bitrate} kbps')
                create_bitrate_txt_file(dirpath, bitrate)
            else:
                error_message = f'Failed to retrieve bitrate for {file_path}\n'
                print(error_message)
                log_error(error_message)

if __name__ == "__main__":
    process_directory_with_V_prefix()