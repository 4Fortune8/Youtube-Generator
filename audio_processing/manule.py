import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from TTS.api import TTS
# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
scp = '035'

speaker='Baldur Sanjin'
item= "Addendum 035 1"
for i in range(0,3):
    tts.tts_to_file(text=item, speaker=speaker, language="en", file_path=f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\audio\\9x {i} {speaker}_output.wav')
            
            
