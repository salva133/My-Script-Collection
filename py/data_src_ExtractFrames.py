"""
Script Name: data_src_ExtractFrames.py
Description: This script is designed to extract frames from video files within a specified directory. It supports a wide range of video formats and allows users to specify the frame extraction rate. The extracted frames are saved in a 'data_src' directory, which is created if it does not already exist. This script is particularly useful in preprocessing steps for video editing and deep learning projects.

Functions:
    get_video_files(cwd) - Retrieves a list of video files in the current working directory, excluding any that start with 'data_'.
    create_data_src_folder() - Creates a 'data_src' folder if it does not already exist.
    get_user_input() - Prompts the user to enter the desired frame extraction rate.
    extract_frames(video_file, fps) - Extracts frames from the specified video file at the specified rate and saves them to the 'data_src' folder.

Variables:
    DEBUG - Boolean flag to toggle debug mode for additional output.
"""


import os
import cv2
import subprocess

DEBUG = False


def get_video_files(cwd):
    """Get a list of all video files in the specified directory."""
    video_extensions = (
        ".mp4",
        ".mov",
        ".mkv",
        ".webm",
        ".avi",
        ".flv",
        ".wmv",
        ".mpeg",
        ".mpg",
        ".m4v",
        ".3gp",
        ".3g2",
        ".ogv",
        ".vob",
    )
    files = [f for f in os.listdir(cwd) if f.endswith(video_extensions)]
    files = [f for f in files if not f.startswith("data_")]
    if DEBUG:
        print(f"Video files to be processed: {files}")
    return files


def create_data_src_folder():
    """Create the "data_src" folder if it doesn't already exist."""
    if not os.path.exists("data_src"):
        os.mkdir("data_src")
        if DEBUG:
            print("Created 'data_src' directory.")


def get_user_input():
    """Get the user input for the frame rate."""
    frames_per_second = input(
        "What every Nth frame of a second should be extracted? Press Enter to extract all frames: "
    )
    return frames_per_second if frames_per_second else None


def extract_frames(video, frames_per_second):
    """Extract frames from a video file using OpenCV and FFmpeg."""
    try:
        cap = cv2.VideoCapture(video)
        if frames_per_second:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    video,
                    "-r",
                    str(frames_per_second),
                    "-q:v",
                    "0",
                    f"data_src/{os.path.splitext(video)[0]}_%05d.jpg",
                ]
            )
        else:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    video,
                    "-q:v",
                    "0",
                    f"data_src/{os.path.splitext(video)[0]}_%05d.jpg",
                ]
            )
        cap.release()
        if DEBUG:
            print(f"Finished processing '{video}'.")
    except Exception as e:
        print(f"An error occurred while processing '{video}': {e}")


def main():
    """Main function to run the script."""
    cwd = os.getcwd()
    video_files = get_video_files(cwd)

    if not video_files:
        raise Exception("No video files found in the current working directory.")

    create_data_src_folder()
    frames_per_second = get_user_input()

    for video in video_files:
        extract_frames(video, frames_per_second)


if __name__ == "__main__":
    main()
