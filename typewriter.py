from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
from pydub import AudioSegment
import re
import pysrt

def parse_srt_file(srt_path, fps):
    subs = pysrt.open(srt_path)
    frame_data = []
    for sub in subs:
        start_seconds = sub.start.ordinal / 1000.0
        end_seconds = sub.end.ordinal / 1000.0
        start_frame = int(start_seconds * fps)
        end_frame = int(end_seconds * fps)
        frame_data.append((start_frame, end_frame, sub.text))
    return frame_data

def create_concat_file(file_list,folder_path, concat_file_path):
    # Create a file listing the audio files in order for FFmpeg concat
    with open(concat_file_path, 'w') as concat_file:
        for file_path in file_list:
            concat_file.write(f"file 'C:\\Users\\Abdul\\Videos\\Youtube\\SCP Channel\\008\\audio\\{file_path}'\n")



def DrawOutline(draw, x, y, text, font, outline_width, outline_fill, text_fill):
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_fill)
    draw.text((x, y), text, font=font, fill=text_fill)
    
    
def get_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0



def create_typewriter_effect(output_dir,fps,folderpath, image_size=(1920, 1080), font_path='arial.ttf', font_size=24, line_height=30):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    frame_data = parse_srt_file('output_subtitles.srt', fps)
    max_lines = 20
    Ystartpix = 800
    Xstartpix = 190
    frame_number = 1
    current_text = []
    mostrecentpos=0
    skiptolines=0
    outline_width = 2
    outlineColor = (0, 0, 0)
    fillColor = (86, 142, 37)
    text = open(folderpath + '\\rawoutput.txt', 'r')
    lines = text.read().split('\n')[:-1]
    for p, data in enumerate(frame_data):
        line=data[2]
        start_frame = data[0]
        end_frame = data[1]  
        img = Image.new('RGBA', image_size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)
        for i in range(skiptolines, p):
            
            if i == skiptolines:
                img = Image.new('RGBA', image_size, color=(0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(font_path, font_size)
            DrawOutline(draw, Xstartpix, Ystartpix+(( i-p-1) * line_height), lines[i], font, outline_width,outlineColor, fillColor)    
        if p > max_lines:
                    skiptolines+=1
        if p == mostrecentpos:
            current_text= []
            for i in range(len(line) + 1):
                current_text.append(line[:i])
                frameperchunk = (end_frame - start_frame) / len(line)

                DrawOutline(draw, Xstartpix, Ystartpix+((0) * line_height), line[:i], font, outline_width, outlineColor, fillColor)                    
                startframe = int(frame_number)
                start = int(startframe)
                end = int(startframe+frameperchunk) 
                
                # Save each frame
                for i in range(start, end):
                    img.save(os.path.join(output_dir, f'frame_{frame_number:04d}.png'))
                    frame_number +=1
            while frame_number < end_frame:
                img.save(os.path.join(output_dir, f'frame_{frame_number:04d}.png'))
                frame_number +=1
        mostrecentpos += 1
            

 
    concat_file_path = 'audio_concat.txt'
    create_concat_file(filelist,folderpath ,concat_file_path)
    
    concat_audio_path = 'concatenated_audio.wav'
    command_concat_audio = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file_path,
        '-c', 'copy',
        concat_audio_path
    ]

    # Run the FFmpeg command to concatenate audio
    subprocess.run(command_concat_audio, check=True)

    # FFmpeg command to create a video from the image sequence and concatenated audio
    command_create_video = [
        'ffmpeg',
        '-framerate', '30', 
        '-i', os.path.join(output_dir, 'frame_%04d.png'), 
        '-i', concat_audio_path,
        '-c:v', 'h264_nvenc',           # Use NVIDIA NVENC for video encoding
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-af', 'afftdn=nf=-20,bass=g=10',  # Apply de-esser and bass enhancement filters
        '-shortest',  # Ensure the video ends when the shortest stream (audio or video) ends
        os.path.join(output_dir, 'typewriter_effect.mp4')]

    # Run the FFmpeg command to create the final video
    subprocess.run(command_create_video, check=True)
    

folderpath = 'C:\\Users\\Abdul\\Videos\\Youtube\\SCP Channel\\008'
output_dir = 'typewriter_frames'
sourcevideo = 'C:\\Users\\Abdul\\Videos\\Youtube\\SCP Channel\\008\\wip'
create_typewriter_effect( output_dir,30,folderpath)
