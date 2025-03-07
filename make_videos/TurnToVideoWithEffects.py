import ffmpeg
import random
import os
import glob
import re
scp='097'
def sort_files(file):
    # Extract the leading number from the file name
    print(os.path.dirname(file))
    match = re.match(r'(\d+)', os.path.dirname(file).split('\\')[-1])
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # If no leading number, place the file at the end


def create_crossfade_video(image_files, output_file):
    transition_duration = 1  # Duration of the fade transition
    inputs =     []
    durationList = []
    image_files = sorted(image_files, key=sort_files)

    for image in image_files:
        probe = ffmpeg.probe(image)
        video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        durationList.append(round(float(video_info['duration'])))
        inputs.append(ffmpeg.input(image))  

    transitions = ['hblur','fade','diagtr','pixelize','diagbl','fadegrays']
    timeelapsed = 0
    # Construct the FFmpeg command
    stream = inputs[0]
    for i in range(1, len(inputs)-1):
        random_transition = random.choice(transitions)
        stream = ffmpeg.overlay(
            stream, ffmpeg.filter(
                (inputs[i],inputs[i+1]),
                'xfade',
                transition=random_transition,
                duration=transition_duration,
                offset=(round(durationList[i])-transition_duration)
                ).setpts(f'PTS-STARTPTS+{(timeelapsed+ durationList[i])}/TB'))
        timeelapsed = timeelapsed + durationList[i]

    stream = ffmpeg.output(stream, output_file, vcodec='libx264', pix_fmt='yuv420p', r=25)

    # Run the FFmpeg command
    ffmpeg.run(stream, overwrite_output=True)

# Usage example
import os
import glob
# Define a custom sorting function


def joinMedia(scp):
    # Define the directory
    directory = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated\\Final'
    fileDict = {}
    # Get a list of all mp4 files in the directory and its subdirectories
    mp4_files = glob.glob(os.path.join(directory, '**', '*.mp4'), recursive=True)
    for file in mp4_files:
        parts = file.split(os.sep)
        for part in parts[-2:]:
            if part.isdigit():
                fileDict[int(part)] = file
    mp4_files = []
    for key in fileDict.keys():
        mp4_files.append(fileDict[key])
    # Print the list of mp4 files


    output_file = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated\\Final\\output-crossfade.mp4'
    mp4_files    = sorted(mp4_files, key=sort_files)
    create_crossfade_video(mp4_files, output_file)


joinMedia(scp)