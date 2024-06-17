import subprocess
import os
import shutil
import json
def get_video_fps(video_path):
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        video_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    video_info = json.loads(result.stdout)

    # Extract fps from the first video stream
    for stream in video_info['streams']:
        if stream['codec_type'] == 'video':
            return eval(stream['avg_frame_rate'])

    return None

def upsample_video(video,output_file,fps):
    os.makedirs(output_file, exist_ok=True)
    command = f'ffmpeg -i {video} -vf "fps={fps}" {output_file}/%03d_frame.png'

    # Execute the command
    subprocess.run(command, shell=True)
    os.makedirs(output_file+"/upscaled", exist_ok=True)
    command = f'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\PostProcess\\realcugan-ncnn-vulkan-20220728-windows\\realcugan-ncnn-vulkan.exe -i {output_file} -o {output_file+"/upscaled"}  -j 4:4:4'
    subprocess.run(command, shell=True)


def interpolate_video(input_file, output_file, ratio, fps):
  

    
    upsample_video(input_file,output_file,fps)
    
    os.makedirs(output_file+"/interpolate", exist_ok=True)
    startframes = len(output_file)
    command = f'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\PostProcess\\rife-ncnn-vulkan-20221029-windows\\rife-ncnn-vulkan.exe -m rife-v4.6 -i {output_file+"\\upscaled"}  -o {output_file+"\\interpolate"}  -j 4:4:4 -n {startframes *ratio/2}'
    subprocess.run(command, shell=True)
    
    output_video_path = output_file + '\\output_video.mp4'
    command = f'ffmpeg -framerate {fps*ratio} -i {output_file+"\\interpolate\\"}%08d.png -c:v libx264 -pix_fmt yuv420p -hwaccel cuda  {output_video_path}'
    subprocess.run(command, shell=True)

def get_video_resolution(video_path):
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        video_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    video_info = json.loads(result.stdout)

    # Extract width and height from the first video stream
    for stream in video_info['streams']:
        if stream['codec_type'] == 'video':
            return stream['width'], stream['height']

    return None, None

def resize_video(input_file, output_file, width, height):
    command = [
        'ffmpeg',
        '-y',
        '-i', input_file,
        '-vf', f'scale={width}:{height},setsar=1',
        'temp.mp4'
    ]
    subprocess.run(command, shell=True)
    shutil.move('temp.mp4', input_file)
    
    
def postprocess(reveservideopath,forwardvideopath,finalpath):
    os.makedirs(finalpath, exist_ok=True)
    # Define the video file path
    video1_path = reveservideopath
    video2_path = forwardvideopath

    video1_FPS = get_video_fps(video1_path)
    video2_FPS = get_video_fps(video2_path)
    video1_res = get_video_resolution(video1_path)
    video2_res = get_video_resolution(video2_path)
    
    resize_video(video1_path, video1_path, 1280,720)
    resize_video(video2_path, video2_path, 1280,720)
    
    output_dir1 = finalpath+'\\frames'
    output_dir2 = finalpath+'\\2frames'
    os.makedirs(output_dir1, exist_ok=True)
    os.makedirs(output_dir2, exist_ok=True)
    if video1_FPS > video2_FPS:
        ratio = video1_FPS / video2_FPS
        upsample_video(video1_path,output_dir1,video1_FPS)
        command = f'ffmpeg -framerate {video1_FPS} -i {output_dir1+"\\upscaled"}/%03d_frame.png -c:v libx264 -pix_fmt yuv420p -hwaccel cuda {output_dir1+"\\output_video.mp4"}'
        subprocess.run(command, shell=True)

        interpolate_video(video2_path, output_dir2, ratio, video2_FPS)
    elif video2_FPS > video1_FPS:
        ratio = video2_FPS / video1_FPS
        upsample_video(video2_path,output_dir2,video2_FPS)
        command = f'ffmpeg -framerate {video2_FPS} -i {output_dir2+"\\upscaled"}/%03d_frame.png -c:v libx264 -pix_fmt yuv420p -hwaccel cuda  {output_dir2+"\\output_video.mp4"}'
        subprocess.run(command, shell=True)
        interpolate_video(video1_path, output_dir1, ratio, video1_FPS)
    elif video1_FPS == video2_FPS and video1_FPS == 6:
        interpolate_video(video1_path, output_dir1, 10, video1_FPS)
        interpolate_video(video2_path, output_dir2, 10, video2_FPS)
    
    output_video_path = os.path.join(finalpath,'output_video.mp4')
    temp_video_path = os.path.join(finalpath,'temp_video.mp4')
    command = f'ffmpeg -i {output_dir1+"\\output_video.mp4"} -vf "reverse" -af "areverse" -hwaccel cuda  {temp_video_path}'

    # Execute the command
    subprocess.run(command, shell=True)

    # Construct the ffmpeg command to concatenate the reversed video and the second video
    
    command =f'ffmpeg -i {temp_video_path} -i {output_dir2+"\\output_video.mp4"} -filter_complex "[0:v] [1:v] concat=n=2:v=1 [v]" -map "[v]" -hwaccel cuda  {output_video_path}'
    # Execute the command
    subprocess.run(command, shell=True)

    # Delete the temporary file
    os.remove(temp_video_path)
    



def solopostprocess(forwardvideopath,finalpath):
    # Define the video file path
    output_video_path = 'output_video.mp4'
    # Delete the temporary file
    video_path = forwardvideopath
    video_FPS = get_video_fps(video_path)    
    resize_video(video_path, video_path, 1280,720)
    # Define the output directory for the frames
    output_dir = finalpath+'\\frames'
    os.makedirs(output_dir, exist_ok=True)
    if video_FPS == 6:
        interpolate_video(video_path, output_dir, 10, video_FPS)
        shutil.move(output_dir+"\\output_video.mp4", finalpath)
    else:
        shutil.copy(forwardvideopath, finalpath+"\\output_video.mp4")
        
    