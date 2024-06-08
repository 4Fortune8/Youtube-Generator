import subprocess
import os
import shutil
def postprocess(reveservideopath,forwardvideopath,finalpath):
    os.makedirs(finalpath, exist_ok=True)
    # Define the video file path
    video1_path = reveservideopath
    video2_path = forwardvideopath
    output_video_path = os.path.join(finalpath,'output_video.mp4')
    temp_video_path = os.path.join(finalpath,'temp_video.mp4')
    command = f'ffmpeg -i {video1_path} -vf "reverse" -af "areverse" {temp_video_path}'

    # Execute the command
    subprocess.run(command, shell=True)

    # Construct the ffmpeg command to concatenate the reversed video and the second video
    
    command =f'ffmpeg -i {temp_video_path} -i {video2_path} -filter_complex "[0:v] [1:v] concat=n=2:v=1 [v]" -map "[v]"  {output_video_path}'
    # Execute the command
    subprocess.run(command, shell=True)

    # Delete the temporary file
    os.remove(temp_video_path)
    video_path = output_video_path

    # Define the output directory for the frames
    output_dir = finalpath+'\\frames'
    os.makedirs(output_dir, exist_ok=True)

    # Construct the ffmpeg command
    command = f'ffmpeg -i {video_path} -vf "fps=6" {output_dir}/%03d_frame.png'

    # Execute the command
    subprocess.run(command, shell=True)
    os.remove(video_path)

    # Define the input and output directories
    input_dir = output_dir
    output_dir = finalpath+'\\output_frames'
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all the image files in the input directory
    image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # For each image file, construct and execute the rife-ncnn-vulkan command
    for image_file in image_files:
        command = f'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\PostProcess\\realcugan-ncnn-vulkan-20220728-windows\\realcugan-ncnn-vulkan.exe -i {os.path.join(input_dir, image_file)} -o {os.path.join(output_dir, image_file)} -g 0  -j 4:4:4'
        subprocess.run(command, shell=True)

    # After processing all the images, delete the input directory
    shutil.rmtree(input_dir)


    # Define the input and output directories
    input_dir = output_dir
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all the image files in the input directory
    image_files = sorted([f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))])

    # For each image file, construct and execute the rife-ncnn-vulkan command
    startframes = len(image_files)
    for pos,image_file in enumerate(image_files[:-1]):
        command = f'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\PostProcess\\rife-ncnn-vulkan-20221029-windows\\rife-ncnn-vulkan.exe -m rife-v4.6 -0 {os.path.join(input_dir, image_files[pos])} -1 {os.path.join(input_dir, image_files[pos+1])} -o {os.path.join(input_dir, f"{pos+1:03}_newframe.png" )} -g 0 -j 4:4:4'
        subprocess.run(command, shell=True)

    image_files = sorted([f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))])
    for i, file in enumerate(image_files):
        # Construct the new file name
        new_file_name = f"{i:03d}_final.png"

        # Define the current file path and the new file path
        current_file_path = os.path.join(input_dir, file)
        new_file_path = os.path.join(input_dir, new_file_name)

        # Use os.rename() to rename the file
        os.rename(current_file_path, new_file_path)


    output_video_path = finalpath + '\\output_video.mp4'
    command = f'ffmpeg -framerate 12 -i {output_dir}/%03d_final.png -c:v libx264 -pix_fmt yuv420p {output_video_path}'
    subprocess.run(command, shell=True)

    shutil.rmtree(input_dir)
    
 

def solopostprocess(forwardvideopath,finalpath):
    # Define the video file path
    video2_path = forwardvideopath
    output_video_path = 'output_video.mp4'

    # Execute the comman

    # Construct the ffmpeg command to concatenate the reversed video and the second video

    # Delete the temporary file
    video_path = forwardvideopath

    # Define the output directory for the frames
    output_dir = finalpath+'\\frames'
    os.makedirs(output_dir, exist_ok=True)

    # Construct the ffmpeg command
    command = f'ffmpeg -i {video_path} -vf "fps=6" {output_dir}/%03d_frame.png'

    # Execute the command
    subprocess.run(command, shell=True)


    # Define the input and output directories
    input_dir = output_dir
    output_dir = finalpath+'\\output_frames'
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all the image files in the input directory
    image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # For each image file, construct and execute the rife-ncnn-vulkan command
    for image_file in image_files:
        command = f'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\PostProcess\\realcugan-ncnn-vulkan-20220728-windows\\realcugan-ncnn-vulkan.exe -i {os.path.join(input_dir, image_file)} -o {os.path.join(output_dir, image_file)} -g 0  -j 4:4:4'        
        subprocess.run(command, shell=True)

    # After processing all the images, delete the input directory
    shutil.rmtree(input_dir)


    # Define the input and output directories
    input_dir =output_dir
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all the image files in the input directory
    # For each image file, construct and execute the rife-ncnn-vulkan command
    startframes = len(image_files)
    for pos,image_file in enumerate(image_files[:-1]):
        command = f'C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\PostProcess\\rife-ncnn-vulkan-20221029-windows\\rife-ncnn-vulkan.exe -m rife-v4.6 -0 {os.path.join(input_dir, image_files[pos])} -1 {os.path.join(input_dir, image_files[pos+1])} -o {os.path.join(input_dir, f"{pos+1:03}_newframe.png" )} -g 0 -j 4:4:4'
        subprocess.run(command, shell=True)

    image_files = sorted([f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))])
    for i, file in enumerate(image_files):
        # Construct the new file name
        new_file_name = f"{i:03d}_final.png"

        # Define the current file path and the new file path
        current_file_path = os.path.join(input_dir, file)
        new_file_path = os.path.join(input_dir, new_file_name)

        # Use os.rename() to rename the file
        os.rename(current_file_path, new_file_path)


    output_video_path = finalpath
    command = f'ffmpeg -framerate 15 -i {output_dir}/%03d_final.png -c:v libx264 -pix_fmt yuv420p {output_video_path}'
    subprocess.run(command, shell=True)

    shutil.rmtree(input_dir)
    
    
