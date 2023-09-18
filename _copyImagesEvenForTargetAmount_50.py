import os
import shutil

# Set a global debug variable to False
DEBUG = False

# Count the total number of image files in the current working directory
total_count = 0
for filename in os.listdir('.'):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        total_count += 1
        if DEBUG: print(f"Found image file: {filename}")

# Initialize the target amount and calculate n
target_amount = 50
n = total_count // target_amount

# Delete the target folder "preview" if it already exists
if os.path.exists('preview'):
    if DEBUG: print("Target folder 'preview' exists. Deleting...")
    shutil.rmtree('preview')

# Create a new target folder "preview"
os.mkdir('preview')
if DEBUG: print("Created new target folder 'preview'.")

# Copy every nth image into the target folder
for i, filename in enumerate(os.listdir('.')):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        if i % n == 0:
            shutil.copy(filename, os.path.join('preview', filename))
            if DEBUG: print(f"Copied {filename} to 'preview' folder.")

# Print a summary of the actions
print(f"A total of {total_count} images were found in the current working directory.")
print(f"Every {n}th image was copied to the 'preview' folder.")
