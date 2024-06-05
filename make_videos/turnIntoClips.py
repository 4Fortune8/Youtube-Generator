import ffmpeg

def crop_video(input_file, overlayVideo, output_file):
    stream = ffmpeg.input(input_file)
    stream_video = ffmpeg.crop(stream.video, '(in_w - in_h)/2', -80, 1000, 1000)
    stream_video = ffmpeg.filter(stream_video, 'scale', 700, -1)

    input_video2 = ffmpeg.input(overlayVideo)
    video2 = ffmpeg.crop(input_video2, '(in_w- in_h)/2', 0, 700, 700)
    video2 = ffmpeg.filter(video2, 'scale', 700, -1)  # Ensure `video2` has the same dimensions as `stream_video`

    # Blend `video2` and `stream_video` together
    blended_video = ffmpeg.filter([stream_video, video2], 'blend', 'overlay' ,shortest = 1)

    # Create the output video with the blended video and the audio from `stream`
    output = ffmpeg.output(blended_video, stream.audio, output_file, f='segment', segment_time='50', reset_timestamps=1)
    ffmpeg.run(output)

scp = '014'
video = f"C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\output.mp4"
clip = f"C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\clip%d.mp4"
overlayVideo  = r'C:\Users\Abdul\VSCODE_Projects\Youtube-Generator\Background\Aids.mp4'

crop_video(video, overlayVideo, clip)