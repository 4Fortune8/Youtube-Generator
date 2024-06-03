import os
import glob
import ffmpeg
import re
# Define a custom sorting function
def sort_files(file):
    # Extract the leading number from the file name
    match = re.match(r'(\d+)', os.path.basename(file))
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # If no leading number, place the file at the end



# Specify the directory
directory = r"C:\Users\Abdul\Videos\Youtube\SCP_Channel\020\RawPhotos"

# Find all .webm files in the directory
webm_files = glob.glob(os.path.join(directory, "*.webp"))
    
# Sort the list of files
webm_files    = sorted(webm_files, key=sort_files)


# Loop over the sorted list of files
for i,webm_file in enumerate(webm_files):
    # Specify the output file
    png_file = directory+"\\" + str(i) + ".png"

    # Convert the .webm file to .png
    stream = ffmpeg.input(webm_file)
    stream = ffmpeg.output(stream, png_file, vframes=1)
    ffmpeg.run(stream)