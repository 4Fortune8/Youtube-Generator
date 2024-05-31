from ComfyUI.ComfyUI_to_Python_Extension.workflow_api_base import AnimatePhoto as AnimatePhotoFast
from ComfyUI.ComfyUI_to_Python_Extension.workflow_api_full import AnimatePhoto as AnimatePhotoUpscaled

import shutil
import os
import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\Imgtovideo\\ComfyUI')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\Imgtovideo\\ComfyUI\\comfy')))


def movephotos(source_dir, dest_dir,folder):
    files = os.listdir(source_dir)
    pastlocation =dest_dir+'//'+folder
    os.makedirs(pastlocation, exist_ok=True)
    # iterate over all files and move each file
    for file in files:
        shutil.move(os.path.join(source_dir, file), pastlocation)

# specify your source directory and destination directory
source_dir = 'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\Imgtovideo\\ComfyUI\\output'
dest_dir = 'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\test'
imgs = os.listdir(dest_dir)
for img in imgs:
    if img.endswith('.png'):    
        for i in range(0,5): 
            timenow= time.time()
            complete = AnimatePhotoFast('C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\test\\'+img,6,30)
            print(time.time()-timenow)
        movephotos(source_dir, dest_dir,img[:-4])
