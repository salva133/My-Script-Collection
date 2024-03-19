"""
Script Name: mergeImageSeq.py
Description: This script compiles a sequence of image files from the current directory into a video file. It supports a variety of image formats and allows for customizable output video names and frame rates. The script is particularly useful for creating video compilations from series of images, such as time-lapse photography or animation frames.

Functions:
    bilder_zu_video(output_name="output.mp4", fps=15) - Compiles image files into a video, with customizable output filename and frames per second.

Usage:
    1. Ensure all image files to be compiled are in the current directory and are of supported formats.
    2. Run the script to compile the images into a video.
    3. The default output video file is 'output.mp4' at 15 fps, but these can be changed by modifying the function parameters.
"""


import imageio
import os


def bilder_zu_video(output_name="output.mp4", fps=15):
    # Liste alle Dateien im aktuellen Verzeichnis auf
    dateien = [f for f in os.listdir() if os.path.isfile(f)]

    # Filtere nur Bilddateien heraus
    bilddateien = [
        f
        for f in dateien
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"))
    ]

    # Sortiere Bilddateien (optional, falls Sie eine bestimmte Reihenfolge möchten)
    bilddateien.sort()

    # Lade alle Bilder
    bilder = [imageio.imread(bild) for bild in bilddateien]

    # Schreibe die Bilder in ein MP4-Video
    imageio.mimsave(output_name, bilder, fps=fps)

    print(f"Video wurde als {output_name} gespeichert.")


if __name__ == "__main__":
    bilder_zu_video()
