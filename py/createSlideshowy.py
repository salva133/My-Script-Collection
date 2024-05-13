import os
import cv2
import numpy as np
from tqdm import tqdm

def resize_image(image, width, height):
    """
    Resize the given image while maintaining the aspect ratio.

    Args:
        image (numpy.ndarray): The image to be resized.
        width (int): The desired width of the resized image.
        height (int): The desired height of the resized image.

    Returns:
        numpy.ndarray: The resized image.
    """
    # Get the image dimensions
    image_height, image_width, _ = image.shape

    # Calculate the aspect ratio of the image
    aspect_ratio = min(width / image_width, height / image_height)

    # Calculate the new dimensions while maintaining the aspect ratio
    new_width = int(image_width * aspect_ratio)
    new_height = int(image_height * aspect_ratio)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    # Create a black background with the specified width and height
    background = np.zeros((height, width, 3), dtype=np.uint8)

    # Calculate the position to paste the resized image on the background
    x = (width - new_width) // 2
    y = (height - new_height) // 2

    # Paste the resized image on the background
    background[y:y+new_height, x:x+new_width] = resized_image
    return background

def merge_images_to_mp4():
    """
    Merge a collection of images into an MP4 video file.

    The images are read from the current working directory and its subdirectories.
    Only files with the extensions '.png', '.jpg', and '.jpeg' are considered as images.

    The merged video file is saved as 'merged_images.mp4' in the current working directory.
    Each image is displayed for 5 seconds in the video.

    Note: This function requires the OpenCV and tqdm libraries to be installed.

    Returns:
        None
    """
    # Get the current working directory
    cwd = os.getcwd()

    # Create a list to store the image file paths
    image_paths = []
    # Iterate through all subdirectories in the current working directory
    for root, dirs, files in os.walk(cwd):
        # Iterate through all files in each subdirectory
        for file in files:
            # Check if the file is an image (you can add more image extensions if needed)
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Get the full file path
                file_path = os.path.join(root, file)
                # Append the file path to the list
                image_paths.append(file_path)

    # Sort the image paths alphabetically
    image_paths.sort()

    # Create a VideoWriter object to write the merged images to an MP4 file
    output_file = "merged_images.mp4"
    frame_rate = 1 / 1
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    width = 0
    height = 0

    # Iterate through the image paths and find the maximum width and height
    for image_path in tqdm(image_paths, desc="Finding maximum width and height"):
        # Read the image
        image = cv2.imread(image_path)
        # Get the image dimensions
        image_height, image_width, _ = image.shape
        # Update the maximum width and height if necessary
        if image_width > width:
            width = image_width
        if image_height > height:
            height = image_height

    # Create a VideoWriter object with the maximum width and height
    video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

    # Iterate through the image paths and write each image to the MP4 file
    for image_path in tqdm(image_paths, desc="Merging images"):
        # Read the image
        image = cv2.imread(image_path)
        # Resize the image to fit the video frame size while maintaining the aspect ratio
        image = resize_image(image, width, height)
        # Write the image to the video file
        video_writer.write(image)

    # Release the VideoWriter object
    video_writer.release()
    
def resize_video(video_path, width, height):
    """
    Resize a video while maintaining the aspect ratio.

    Args:
        video_path (str): The path to the video file.
        width (int): The desired width of the resized video.
        height (int): The desired height of the resized video.

    Returns:
        None
    """
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Get the video frame dimensions
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the aspect ratio of the video
    aspect_ratio = min(width / frame_width, height / frame_height)

    # Calculate the new dimensions while maintaining the aspect ratio
    new_width = int(frame_width * aspect_ratio)
    new_height = int(frame_height * aspect_ratio)

    # Create a VideoWriter object to write the resized video
    output_file = "resized_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, (new_width, new_height))

    # Read and resize each frame of the video
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (new_width, new_height))
        video_writer.write(resized_frame)

    # Release the VideoCapture and VideoWriter objects
    video_capture.release()
    video_writer.release()

    # Remove the original video file
    os.remove(video_path)

    # Rename the resized video file to the original video file name
    os.rename(output_file, video_path)

# Call the function to merge images to MP4
if __name__ == "__main__":
    merge_images_to_mp4()
    resize_video("merged_images.mp4", 1280, 720)