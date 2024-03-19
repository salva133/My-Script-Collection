"""
Script Name: data_src_ScanAllVideosForFrameCount.py
Description: This script scans all video files in the current working directory to count the number of frames in each video. It supports multiple video formats and ensures that only videos not prefixed with 'data_' are processed. The script is useful for analyzing and organizing video data before deep learning processing or video editing tasks.

Functions:
    check_video_files() - Scans the current working directory for video files in supported formats, excluding those prefixed with 'data_'.
    check_extracted_folder() - Verifies the presence of the 'extracted' folder and lists its image files.
    get_frame_count(video_file) - Counts and returns the number of frames in the specified video file.

Variables:
    DEBUG - Boolean flag to toggle debug mode for additional output.
"""


import os
import cv2

DEBUG = False


def check_video_files():
    video_files = [
        f
        for f in os.listdir()
        if f.endswith(
            (
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
        )
        and not f.startswith("data_")
    ]
    if not video_files:
        raise Exception("There are no video files in the current working directory!")
    if DEBUG:
        print(f"Video files to be processed: {video_files}")
    return video_files


def check_extracted_folder():
    if os.path.isdir("extracted"):
        extracted_files = [
            f
            for f in os.listdir("extracted")
            if f.endswith(".jpg") or f.endswith(".png")
        ]
        if extracted_files:
            print("WARNING: The folder 'extracted' already contains image files.")


def calculate_total_seconds(video_files):
    total_seconds = 0
    for file in video_files:
        cap = cv2.VideoCapture(file)
        total_seconds += int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        )
        cap.release()
    return total_seconds


def print_total_seconds(total_seconds):
    print("Total number of seconds of the videos: ", total_seconds)


def print_multiple_seconds(total_seconds):
    for i in range(2, 16):
        multiple_seconds = total_seconds * i
        if len(str(multiple_seconds)) > 5:
            print("\nFrame amounts over 5 digits are not recommended!")
            break
        print("              ", i, "Frames per second: ", multiple_seconds)


def print_end_message():
    print("\n\n      #  Counting completed.  #      \n\n")


def main():
    video_files = (
        check_video_files()
    )  # Check for video files in the current working directory
    check_extracted_folder()  # Check if 'extracted' folder exists and if it contains image files
    total_seconds = calculate_total_seconds(
        video_files
    )  # Calculate the total seconds of the videos
    print_total_seconds(
        total_seconds
    )  # Print the total number of seconds of the videos
    print_multiple_seconds(
        total_seconds
    )  # Print the total seconds of the videos multiplied by 2-15
    print_end_message()  # Print the end message indicating the completion of counting


if __name__ == "__main__":
    main()
