import subprocess
import os
import re
from pydub import AudioSegment


def get_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0


def getlenthoftime(proj_path):
    # Open a directory
    dir_path = proj_path+'\\audio'
    files = os.listdir(dir_path)
    print(f'Files in directory: {files}')

# Sort the files by number
    sorted_files = sorted(files, key=get_number)

    print(sorted_files)
    # Get the length of an audio clip
    totaltime = 0
    for file in sorted_files:
        audio_path = dir_path+ '/' + file
        audio = AudioSegment.from_wav(audio_path)
        totaltime += audio.duration_seconds
        print(f'File: {file}, Duration: {int(duration)}')
        
    return totaltime, sorted_files



def create_video_with_ffmpeg(image_path, audio_path, output_path, duration):
    # Create filter for text overlay if provided
    text_filter = ''

    # FFmpeg command to create a video from an image with an audio background and text overlay
    command = [
        'ffmpeg',
        '-loop', '1',                   # Loop the image
        '-i', image_path,               # Input image
        '-stream_loop', '-1',           # Loop the audio
        '-i', audio_path,               # Input audio
        '-c:v', 'libx264',              # Video codec
        '-t', str(duration),            # Duration of the video
        '-pix_fmt', 'yuv420p',          # Pixel format
        '-vf', f"scale=1920:1080,{text_filter}" if text_filter else 'scale=1920:1080', # Scale and optionally add text
        '-c:a', 'aac',                  # Audio codec
        '-b:a', '192k',                 # Audio bitrate
        '-filter:a', 'loudnorm=I=-16:LRA=11:TP=-1.5',  # Normalize audio to -16 dB
        '-shortest',                    # Finish encoding when the shortest input ends
        output_path                     # Output file
    ]

    # Run the FFmpeg command
    subprocess.run(command, check=True)

# Usage example

    
    
# Usage example
image_path = 'C:\\Users\\Abdul\\Videos\\Youtube\\FFmpeg\\BackgroundCrop.jpg'
audio_path = 'C:\\Users\\Abdul\\Videos\\Youtube\\FFmpeg\\from-beyond-royalty-free-no-copyright-background-music(1).wav'
output_path = 'C:\\Users\\Abdul\\Videos\\Youtube\\FFmpeg\\output_video.mp4'
overlay_path = 'C:\\Users\\Abdul\\Videos\\Youtube\\FFmpeg\\overlay.mp4'  # Path to the overlay image/video
duration,audiofiles = getlenthoftime('C:\\Users\\Abdul\\Videos\\Youtube\\SCP Channel\\008')

create_video_with_ffmpeg(image_path, audio_path, output_path, duration)
