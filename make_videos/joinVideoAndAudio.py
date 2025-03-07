import ffmpeg
import random
import os
import glob
import math
import subprocess
import tempfile
import auto_subtitle 


def buildVideo(backroundAudio, VoiceAudio,Video,finalpath):
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_file2 = tempfile.NamedTemporaryFile(suffix=".mp4",delete=False)
    input_video = ffmpeg.input(Video, hwaccel='cuda')
    
    input_audio1 = ffmpeg.input(VoiceAudio, hwaccel='cuda')
    input_audio2 = ffmpeg.input(backroundAudio, hwaccel='cuda',stream_loop=-1)

    # Cut out the first 8 seconds of the audio
    # Get the duration of the first audio file
    audio1_duration = float(ffmpeg.probe(VoiceAudio)['streams'][0]['duration'])
  

    # Repeat the second audio file until it's as long as the first audio file
    audio2 = input_audio2.audio.filter_('atrim', duration=audio1_duration).filter_('loudnorm', I=-34, LRA=11, TP=-1.5)
 

    # Mix the two audio streams
    audio = ffmpeg.filter_([input_audio1.audio, audio2], 'amix')

    output = ffmpeg.output(input_video.video, input_audio1.audio, temp_file.name, shortest=None, vcodec='h264_nvenc')
    ffmpeg.run(output, overwrite_output=True)
    
   
    subprocess.run(['auto_subtitle', temp_file.name, '--model', 'medium.en', '-o', './thing','--srt_only',"True"])
    
    subprocess.run(['ffmpeg','-hwaccel','cuda', '-i', temp_file.name,"-c:v", "h264_nvenc", '-vf', 'subtitles=./thing/subtitles.srt ', '-y', temp_file2.name]) 
    
    input_video = ffmpeg.input(temp_file2.name, hwaccel='cuda')
    # Combine the video and the mixed audio
    output = ffmpeg.output(input_video.video, audio, finalpath+'\output.mp4', shortest=None, vcodec='h264_nvenc')
    
    
  
    # Run the command
    ffmpeg.run(output, overwrite_output=True)
    
scp = '020'
baseDir= f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}'
audio= baseDir+'\\concatenated_audio.wav'
video = f"C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated\\Final\\output-crossfade.mp4"

backroundAudio = r'C:\Users\Abdul\VSCODE_Projects\Youtube-Generator\Background\from-beyond-royalty-free-no-copyright-background-music(1).wav'
buildVideo(backroundAudio,audio,video,baseDir)
