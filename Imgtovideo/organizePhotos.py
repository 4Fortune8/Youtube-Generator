import os
import shutil

# Define the parent directory
parent_dir = r'C:\Users\Abdul\Videos\Youtube\SCP_Channel\035\photos'

# Initialize a counter
counter = 0

# For each subdirectory in the parent directory
for subdir, dirs, files in os.walk(parent_dir):
    # For each file in the subdirectory
    for file in files:
        # If the file is a photo
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # Construct the new file path
            new_file_path = os.path.join(parent_dir, f'{counter}.png')
            
            # Move the file
            shutil.move(os.path.join(subdir, file), new_file_path)
            
            # Increment the counter
            counter += 1
