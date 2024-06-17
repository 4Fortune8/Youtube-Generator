
import shutil
import os
import time
import subprocess
import sys
import re
sys.path.insert(0, r'C:\Users\Abdul\VSCODE_Projects\Youtube-Generator')

import pickle

state_file = 'state.pkl'

from PostProcess.postprocess import postprocess, solopostprocess

def save_state(state):
    with open(state_file, 'wb') as f:
        pickle.dump(state, f)

def load_state():
    if os.path.exists(state_file):
        with open(state_file, 'rb') as f:
            return pickle.load(f)
    else:
        return None
    
state = load_state()
if state is not None:
    # Continue from where you left off
    pass

#from make_videos.TurnToVideoWithEffects import joinMedia
# Define a custom sorting function
def sort_files(file):
    # Extract the leading number from the file name
    match = re.match(r'(\d+)', os.path.basename(file))
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # If no leading number, place the file at the end

def movephotos(source_dir, dest_dir):
    files = os.listdir(source_dir)
    pastelocation =dest_dir
    os.makedirs(pastelocation, exist_ok=True)
    # iterate over all files and move each file
    for file in files:
        shutil.move(os.path.join(source_dir, file), pastelocation)
scp = '035'
# specify your directory
root_dir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated'
otherroot_dir = f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\animated'
# list to store file paths

folders = [name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]
folders = sorted(folders, key=sort_files)

file_paths = {}
n=0
reverse = False
forward = False
# walk through the directories
for folder in folders:
    for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, folder)):
        filenames = sorted(filenames, key=sort_files)

        for filename in filenames:
            if filename.endswith('.mp4'):
                # construct the full file path
                file_path = os.path.join(dirpath, filename)
                
                # play the file with VLC
                
                if filename[0]== 'r':
                    reverse = file_path
                if filename[0] == 'f':
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
    fps =6
    save_state(state)
    try:
        file_paths[file_path][1]
        postprocess(file_paths[file_path][0],file_paths[file_path][1],finalvideos )
    except:
        solopostprocess(file_paths[file_path][0],finalvideos )
    os.makedirs(finalvideos, exist_ok=True)



#joinMedia(scp)

   