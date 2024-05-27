import os
import cv2
import numpy as np
from tqdm import tqdm

def find_image_files(directory, extensions=('.png', '.jpg', '.jpeg'), sort_by='name', ascending=False):
    """Find and sort image files in the given directory and its subdirectories."""
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                full_path = os.path.join(root, file)
                image_paths.append(full_path)

    # Sorting logic based on the 'sort_by' parameter
    if sort_by == 'name':
        image_paths.sort(key=lambda x: os.path.basename(x).lower(), reverse=not ascending)
    
    return image_paths

def resize_image(image, width, height):
    """Resize the given image while maintaining the aspect ratio."""
    image_height, image_width, _ = image.shape
    aspect_ratio = min(width / image_width, height / image_height)
    new_width = int(image_width * aspect_ratio)
    new_height = int(image_height * aspect_ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    background = np.zeros((height, width, 3), dtype=np.uint8)
    x = (width - new_width) // 2
    y = (height - new_height) // 2
    background[y:y+new_height, x:x+new_width] = resized_image
    return background

def create_video_from_images(image_paths, output_filename, frame_size, frame_rate=0.2):
    """Create a video from a list of images."""
    video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, frame_size)
    for path in tqdm(image_paths):
        image = cv2.imread(path)
        image = resize_image(image, *frame_size)
        video_writer.write(image)
    video_writer.release()

def resize_video(video_path, new_width, new_height):
    """Resize a video while maintaining the aspect ratio."""
    video_capture = cv2.VideoCapture(video_path)
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    aspect_ratio = min(new_width / frame_width, new_height / frame_height)
    scaled_width = int(frame_width * aspect_ratio)
    scaled_height = int(frame_height * aspect_ratio)
    output_file = "resized_" + os.path.basename(video_path)
    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), video_capture.get(cv2.CAP_PROP_FPS), (scaled_width, scaled_height))
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (scaled_width, scaled_height))
        video_writer.write(resized_frame)
    video_capture.release()
    video_writer.release()
    os.rename(output_file, video_path)

if __name__ == "__main__":
    images_dir = os.getcwd()  # Der Ordner, in dem nach Bildern gesucht wird
    # Findet und sortiert die Bilder alphabetisch absteigend
    image_files = find_image_files(images_dir, sort_by='name', ascending=False)
    video_filename = 'merged_images.mp4'
    frame_dimensions = (1920, 1080)  # Maximale Bildgröße
    create_video_from_images(image_files, video_filename, frame_dimensions)
    resize_video(video_filename, 1280, 720)