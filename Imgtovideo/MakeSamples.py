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


scp = '100'

photoLocationDir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\photos\\'
animationOutoutDir = 'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\Imgtovideo\\ComfyUI\\output'
dest_dir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated'
def makeSamples(photolocationDir,animationOutoutDir, destDir):
    imgs = os.listdir(photoLocationDir)
    for img in imgs[1:]:
        if img.endswith('.png'):    
            for i in range(0,4): 
                timenow= time.time()
                complete = AnimatePhotoFast(photoLocationDir+img,6,30)
                print(time.time()-timenow)
            movephotos(animationOutoutDir, destDir,img[:-4])

if __name__ == "__main__":             
    makeSamples(photoLocationDir,animationOutoutDir, dest_dir)


