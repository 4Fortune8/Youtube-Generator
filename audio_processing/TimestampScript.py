import os
from pydub import AudioSegment
import pysrt

import re

def get_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

def getlenthoftime(proj_path,fps=480):
    # Open a directory
    dir_path = proj_path+'\\audio'
    files = os.listdir(dir_path)
    print(f'Files in directory: {files}')

# Sort the files by number
    sorted_files = sorted(files, key=get_number)

    print(sorted_files)
    # Get the length of an audio clip
    lengthlist = []
    for file in sorted_files:
        audio_path = dir_path+ '/' + file
        audio = AudioSegment.from_wav(audio_path)
        duration = audio.frame_count()
        frame_rate = audio.frame_rate
        
        duration_seconds = duration / frame_rate
        frames = round(duration_seconds * fps)
        print(f'File: {file}, Duration: {int(frames)} frames, Frame rate: {duration_seconds * fps} frames per second, Duration: {duration_seconds} seconds')
        lengthlist.append(int(frames))
   
    return sorted_files

def seconds_to_subrip_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return pysrt.SubRipTime(hours, minutes, seconds)



def get_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000.0  # duration in seconds

def create_srt_file(audio_dir, text_chunks, output_srt, aduio_list):
    subs = pysrt.SubRipFile()
    start_time = 0.0

    for i, text in enumerate(text_chunks):
        audio_path = os.path.join(audio_dir, f"{aduio_list[i]}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file {audio_path} not found.")

        duration = get_audio_duration(audio_path)
        end_time = start_time + duration
        print(f"Start time: {start_time}, End time: {end_time}")
        start_time_str = seconds_to_subrip_time(start_time)
        end_time_str = seconds_to_subrip_time(end_time)
        print(f"Start time: {start_time_str}, End time: {end_time_str}")

        sub = pysrt.SubRipItem(index=i+1, start=start_time_str, end=end_time_str, text=text)
        subs.append(sub)

        start_time = end_time

    subs.save(output_srt, encoding='utf-8')

# Usage example
audio_dir = 'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\009\\audio'
text_chunks = [
    ]
output_srt = 'output_subtitles.srt'

folderpath = 'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\009'
text = open(folderpath + '\\rawoutput.txt', 'r')
for line in text:
    text_chunks.append(line)
print(text_chunks)

audiolist = getlenthoftime(folderpath)

create_srt_file(audio_dir, text_chunks, output_srt, audiolist)
