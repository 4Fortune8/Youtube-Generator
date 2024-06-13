from ComfyUI.ComfyUI_to_Python_Extension.workflow_api_base import AnimatePhoto as AnimatePhotoFast

import shutil
import os
import sys
import time
import ffmpeg
from PIL import Image
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\Imgtovideo\\ComfyUI')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\Imgtovideo\\ComfyUI\\comfy')))

def movephotos(source_dir, dest_dir,folder):
    files = os.listdir(source_dir)
    pastlocation =dest_dir+'//'+folder
    os.makedirs(pastlocation, exist_ok=True)
    # iterate over all files and move each file
    for file in files:
        shutil.move(os.path.join(source_dir, file), pastlocation)


scp = '035'

photoLocationDir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\photos\\'
animationOutoutDir = 'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\Imgtovideo\\ComfyUI\\output'
dest_dir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated'
def makeSamples(photolocationDir,animationOutoutDir, destDir):
    imgs = os.listdir(photoLocationDir)
    for img in imgs[:18]:
        if img.endswith('.png'):
            imgDir = photoLocationDir+img
            output=destDir+"\\"+img[:-4]+"\\"
            os.makedirs(output, exist_ok=True)
            makeStaticEffects(imgDir, output)
            for i in range(0,4): 
                timenow= time.time()
                complete = AnimatePhotoFast(photoLocationDir+img,6,30)
                print(time.time()-timenow)

                
            movephotos(animationOutoutDir, destDir,img[:-4])

def makeStaticEffects(imgDir, output):
            duration = 7  # duration of the video in seconds
            frame_rate = 60  # frame rate of the video

            # Get the width of the image
            with Image.open(imgDir) as img:
                img_width = img.width
                img_height = img.height
            # Calculate the width of the crop rectangle
            crop_width = 1280
            crop_height = 720
            initial_y = img_height - crop_height

            # Calculate the total number of frames in the video
            total_frames = duration * frame_rate

            # Calculate the pan speed
            pan_speed_horizontal = (crop_width) / total_frames
            pan_speed_vertical = (crop_height) / total_frames
        
            zoomout(imgDir,output,duration)
            panleft(imgDir,output,crop_width,crop_height,duration,frame_rate,pan_speed_horizontal,img_width)
            panright(imgDir,output,crop_width,crop_height,duration,frame_rate,pan_speed_horizontal,img_width)
            panup(imgDir,output,crop_width,crop_height,duration,frame_rate,pan_speed_vertical,initial_y)
            pandown(imgDir,output,crop_width,crop_height,duration,frame_rate,pan_speed_vertical)

def zoomin(imgPath, outputDir,duration):
    input_stream = ffmpeg.input(imgPath,t=duration ,hwaccel='cuda')
    output_stream = input_stream.output(f'{outputDir}zoomin.mp4', vf='zoompan=z=\'zoom+0.0031\':x=\'iw*0.10\':y=\'ih*0.10\'')
    ffmpeg.run(output_stream)

def zoomout(imgPath, outputDir,duration):#makes a zoom in vidoe then reverses it
    zoomin(imgPath, outputDir,duration)
    input_stream = ffmpeg.input(f'{outputDir}zoomin.mp4', hwaccel='cuda')
    output_stream = input_stream.output(f'{outputDir}zoomout.mp4', vf='reverse')
    ffmpeg.run(output_stream)
    
def panright(imgPath, outputDir, crop_width, crop_height,duration,frame_rate,pan_speed,img_width):
    max_n = (img_width / 2 - crop_width) / pan_speed
    input_stream = ffmpeg.input(imgPath, loop=1, t=duration, hwaccel='cuda')
    output_stream = input_stream.output(outputDir+"panright.mp4", vf=f'crop={crop_width}:{crop_height}:(n*{pan_speed*1.2}):0', r=frame_rate/2)
    ffmpeg.run(output_stream)
    
def panleft(imgPath, outputDir, crop_width, crop_height,duration,frame_rate,pan_speed,img_width):
    input_stream = ffmpeg.input(imgPath, loop=1, t=duration, hwaccel='cuda')
    output_stream = input_stream.output(outputDir+"panleft.mp4", vf=f'crop={crop_width}:{crop_height}:(in_w-{crop_width}-n*{pan_speed*1.2}):0', r=frame_rate)
    ffmpeg.run(output_stream)
    
def panup(imgPath, outputDir, crop_width, crop_height,duration,frame_rate,pan_speed,intial_y):
    input_stream = ffmpeg.input(imgPath, loop=1, t=duration, hwaccel='cuda')
    output_stream = input_stream.output(outputDir+"panup.mp4", vf=f'crop={crop_width}:{crop_height}:220:({intial_y}-n*{pan_speed*1.2})', r=frame_rate)
    ffmpeg.run(output_stream)
    
   
def pandown(imgPath, outputDir, crop_width, crop_height,duration,frame_rate,pan_speed):
    input_stream = ffmpeg.input(imgPath, loop=1, t=duration, hwaccel='cuda')
    output_stream = input_stream.output(outputDir+"pandown.mp4", vf=f'crop={crop_width}:{crop_height}:220:(n*{pan_speed*1.2})', r=frame_rate)
    ffmpeg.run(output_stream)



    
if __name__ == "__main__":           
    makeSamples(photoLocationDir,animationOutoutDir, dest_dir)


