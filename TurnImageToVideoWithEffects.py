import ffmpeg
import random

def create_crossfade_video(image_files, output_file):
    duration_per_image = 5  # Duration each image is shown
    transition_duration = 1  # Duration of the fade transition

    inputs = [ffmpeg.input(image, loop=1, t=duration_per_image) for image in image_files]

    transitions = ['hblur','fade','diagtr','pixelize','diagbl','fadegrays']
    
    # Construct the FFmpeg command
    stream = inputs[0]
    for i in range(1, len(inputs)):
        random_transition = random.choice(transitions)
        stream = ffmpeg.overlay(stream, ffmpeg.filter((inputs[i-1],inputs[i]), 'xfade', transition=random_transition, duration=transition_duration, offset=(transition_duration-0.5)).setpts(f'PTS-STARTPTS+{i * duration_per_image-transition_duration}/TB'))

    stream = ffmpeg.output(stream, output_file, vcodec='libx264', pix_fmt='yuv420p', r=25)

    # Run the FFmpeg command
    ffmpeg.run(stream, overwrite_output=True)

# Usage example
image_files = [
    'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\photos\\image_0001.png',
    'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\photos\\image_0002.png',
    'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\photos\\image_0003.png',
    'C:\\Users\\Abdul\\VSCODE Projects\\Youtube-Generator\\photos\\image_0004.png',
]
output_file = 'output-crossfade.mp4'

create_crossfade_video(image_files, output_file)
