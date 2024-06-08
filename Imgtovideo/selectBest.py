
import shutil
import os
import time
import subprocess
import sys

sys.path.insert(0, r'C:\Users\Abdul\VSCODE_Projects\Youtube-Generator')


from PostProcess.postprocess import postprocess, solopostprocess
#from make_videos.TurnToVideoWithEffects import joinMedia

def movephotos(source_dir, dest_dir):
    files = os.listdir(source_dir)
    pastelocation =dest_dir
    os.makedirs(pastelocation, exist_ok=True)
    # iterate over all files and move each file
    for file in files:
        shutil.move(os.path.join(source_dir, file), pastelocation)
scp = '096'

# specify your directory
root_dir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated'
otherroot_dir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated'
# list to store file paths
file_paths = {}
n=0
reverse = False
forward = False
# walk through the directories
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        
        # check if the file is an mp4 file
        if filename.endswith('.mp4'):
            # construct the full file path
            file_path = os.path.join(dirpath, filename)
            
            # play the file with VLC
            subprocess.call([r'C:\Program Files\VideoLAN\VLC\vlc.exe', '--play-and-exit', file_path])            # ask the user if they want to add the file to the list
            answer = input('Do you want to add this file to the list? (r/f/n) ')
            if answer.lower() == 'r':
                reverse = file_path
            if answer.lower() == 'f':
                forward = file_path
    if forward and reverse:
                file_paths[n] = [reverse, forward]
                n+=1
                reverse = False
                forward = False
    if forward:
                file_paths[n] = [forward]
                n+=1
                forward = False

# print the list of file paths
for file_path in file_paths:
    file_path_parts = file_paths[file_path][0].split('\\')
    print(file_path_parts)
    print(file_path_parts[-1])
    print(file_path_parts[-2])
    
    finalvideos =os.path.join(root_dir,'Final',file_path_parts[-2])
    generatevalues = file_path_parts[-1].split('_')
    fps =generatevalues[-2]
    try:
        file_paths[file_path][1]
        postprocess(file_paths[file_path][0],file_paths[file_path][1],finalvideos )
    except:
        solopostprocess(file_paths[file_path][0],finalvideos )
    os.makedirs(finalvideos, exist_ok=True)



#joinMedia(scp)

   