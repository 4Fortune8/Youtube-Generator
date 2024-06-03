from melo.api import TTS
model = TTS(language='EN', use_hf=False)
import os
import glob
import sys


speakers = "EN-UK"
speaker_ids = model.hps.data.spk2id


save_dir = r'C:\Users\Abdul\VSCODE_Projects\Youtube-Generator\audio_processing'
texts = 'contaminated various liquids, including ice... steam... tea... fruit juice... seawater,, and blood..... The time for contamination varied from 3 minutes to several hours, depending on temperature and composition........... This rapid assimilation poses a significant threat if'
speed = 0.91
output_path = f'{save_dir}/EN-BR/speed_{speed}/sent_{1:03d}.wav'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
model.tts_to_file(texts, speaker_ids['EN-BR'], output_path, speed=speed)