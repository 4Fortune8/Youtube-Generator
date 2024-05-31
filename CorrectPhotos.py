import os
from PIL import Image

def crop_and_save_images(input_dir, output_dir):
    for i,filename in enumerate(os.listdir(input_dir)):
        if filename.endswith(".webp"):
            img = Image.open(os.path.join(input_dir, filename))
            width, height = img.size

            # Calculate dimensions for 16:9 aspect ratio
            new_width = min(width, height * 16 / 9)
            new_height = new_width * 9 / 16

            # Calculate the area to crop
            left = (width - new_width) / 2
            top = (height - new_height) / 2
            right = (width + new_width) / 2
            bottom = (height + new_height) / 2

            # Crop the image and save it as a PNG
            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(os.path.join(output_dir, str(i) + '.png'))

# Use the function
crop_and_save_images('C:\\Users\\Abdul\\Videos\\Youtube\\SCP Channel\\009\\Photos', 'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\test')