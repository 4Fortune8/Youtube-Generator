
import os
import subprocess
import argparse

# Get the list of image files
input_dir = r'C:\Users\Abdul\Videos\Youtube\SCP_Channel\035\photos'
image_files = sorted(os.listdir(input_dir))

# Create the output directory
output_dir = os.path.join(input_dir, 'upscaled')
os.makedirs(output_dir, exist_ok=True)

# For each pair of consecutive images
for pos, image_file in enumerate(image_files[:-1]):
    # Construct the command
    command =f'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\PostProcess\\realcugan-ncnn-vulkan-20220728-windows\\realcugan-ncnn-vulkan.exe -i {os.path.join(input_dir, image_file)} -o {os.path.join(output_dir, str(pos)+".png")} -g 0  -j 4:4:4' 
    
    # Run the command
    subprocess.run(command, shell=True)