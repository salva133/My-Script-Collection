"""
Script Name: copyImagesEvenForTargetAmount_50.py
Description: This script evenly distributes a set number of image files into a target directory named 'extracted'. Specifically, it is designed to select every nth image from the current working directory (where n is determined by the total number of images divided by the target amount) until 50 images have been selected. Supported image formats include JPG, JPEG, and PNG.

Workflow:
    1. Count the total number of supported image files in the current directory.
    2. Calculate the step size (n) by dividing the total number of images by the target amount (50).
    3. Delete the existing 'extracted' folder if it exists, and create a new one.
    4. Copy every nth image file into the 'extracted' folder.

Variables:
    DEBUG - Flag to enable or disable debug mode for additional output during script execution.
"""


import os
import shutil

# Set a global debug variable to False
DEBUG = False

# Count the total number of image files in the current working directory
total_count = 0
for filename in os.listdir("."):
    if (
        filename.endswith(".jpg")
        or filename.endswith(".jpeg")
        or filename.endswith(".png")
    ):
        total_count += 1
        if DEBUG:
            print(f"Found image file: {filename}")

# Initialize the target amount and calculate n
target_amount = input("Declare the target amount you want to get out of the source: ")
target_amount = int(target_amount)
n = total_count // target_amount

# Delete the target folder "extracted" if it already exists
if os.path.exists("extracted"):
    if DEBUG:
        print("Target folder 'extracted' exists. Deleting...")
    shutil.rmtree("extracted")

# Create a new target folder "extracted"
os.mkdir("extracted")
if DEBUG:
    print("Created new target folder 'extracted'.")

# Copy every nth image into the target folder
for i, filename in enumerate(os.listdir(".")):
    if (
        filename.endswith(".jpg")
        or filename.endswith(".jpeg")
        or filename.endswith(".png")
    ):
        if i % n == 0:
            shutil.copy(filename, os.path.join("extracted", filename))
            if DEBUG:
                print(f"Copied {filename} to 'extracted' folder.")

# Print a summary of the actions
print(f"A total of {total_count} images were found in the current working directory.")
print(f"Every {n}th image was copied to the 'extracted' folder.")
