import ffmpeg

def crop_video(input_file, output_file):
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.crop(stream, '(in_w - in_h)/2', 0, 'in_h', 'in_h')
    output_stream = ffmpeg.output(stream, output_file, f='segment', segment_time='50', reset_timestamps=0, map='0:a')
    ffmpeg.run(output_stream)


# Usage
video = r"C:\Users\Abdul\Videos\Youtube\SCP_Channel\009\output.mp4"

clip = r"C:\Users\Abdul\Videos\Youtube\SCP_Channel\009\clip%d.mp4"

crop_video(video, clip)  # For a 9:16 aspect ratio