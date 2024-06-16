from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
from pydub import AudioSegment
import re
import glob


def create_concat_file(file_list, concat_file_path): #Todo
    # Create a file listing the audio files in order for FFmpeg concat
    with open(concat_file_path, 'w') as concat_file:
        for file_path in file_list:
            if file_path[-3:] == 'wav':
                concat_file.write(f"file '{file_path}'\n")




# Define a custom sorting function
def sort_files(file):
    # Extract the leading number from the file name
    match = re.match(r'(\d+)', os.path.basename(file))
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # If no leading number, place the file at the end



def joinAudio(baseDir):
    directory = baseDir+'\\Audio'
    # Sort the files using the custom sorting function
    # Get a list of all mp4 files in the directory
    concat_file_path = 'audio_concat.txt'
    mp4_files = glob.glob(os.path.join(directory, '*.wav'))
    mp4_files = sorted(mp4_files, key=sort_files)
    print(mp4_files)
    create_concat_file(mp4_files ,concat_file_path)
    concat_audio_path = baseDir+'\concatenated_audio.wav'
    command_concat_audio = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file_path,
        '-c', 'copy',
        '-af', ' highpass=f=320,lowpass=f=7200, volume=1.10,afftdn , atempo=1.01',
        '-c:a', 'pcm_s16le',
        concat_audio_path
    ]
    
    # Run the FFmpeg command to concatenate audio
    subprocess.run(command_concat_audio, check=True)
    # FFmpeg command to create a video from the image sequence and concatenated audio
scp = '035'
baseDir= f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}'
joinAudio(baseDir)
