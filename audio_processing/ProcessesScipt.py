import re 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from TTS.api import TTS
# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
scp = '097'
replacements = {
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "Mrs.": "Missus",
    "(In a calm, robotic tone)": "",
    "Welcome, test subjects": "Welcome, Site Director",

    "%": " percent",
    "°C": " degrees Celsius",
    "°F": " degrees Fahrenheit",
    "m³": " cubic meters",
    '████' : 'redacted',
    '██' : 'redacted',
    # Add more replacements as needed
}

rawreplacements = {
    "Keter": 'ketter',
    "SCP": 'Es-C-P',
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "Mrs.": "Missus",
    "(In a calm, robotic tone)": "",
    "Welcome, test subjects": "Welcome, Site Director",
    "°C": " degrees Celsius",
    "°F": " degrees Fahrenheit",
    "m³": " cubic meters",
    '███████' : 'redacted,',
    '██████' : 'redacted,',
    '█████' : 'redacted,',
    '████' : 'redacted,',
    '███' : 'redacted,',
    '██' : 'redacted,',
    '█' : 'redacted,',
   # '.': '...',
   # ',': '.'
}
promptreplacements = {

}
def replace_all(text, dic):
    for old, new in dic.items():
        text = text.replace(old, new)
    text = re.sub(r'(?<=\s)-(?!\D)', 'negative ', text)
    text = re.sub(r'(\d+)x(\d+)', r'\1 by \2', text)
    text = re.sub(r'\.\s*"', '"', text)
    text = re.sub(f'{scp}-', f'{scp} ', text)    
    return text

listoflines = []
listofrawlines =[] 
listofpromptlines =[]

speaker='Baldur Sanjin'
with open(f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\script.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    
    
for pos, line in enumerate(lines):
    rawline = replace_all(line, rawreplacements)
    line= replace_all(line, replacements)     
    if 'GLaDOS' in line and line[0] != '[':
        rawline =rawline.split(':', 1)[1]
        rawsentence = re.split('[:]', rawline)
        listofrawlines.extend(rawsentence)
        line = line.split(':', 1)[1]
        listofpromptlines.append(line)
        sentences = re.split('[,.:]', line)
        listoflines.extend(sentences)
    elif '[Test Proposal' in line:
        rawsentence = re.split('[,.:]', rawline)
        rawsentence[0] = rawsentence[0].lstrip('[')
        rawsentence[1] = rawsentence[1].rstrip(']\n')
        listofrawlines.extend(rawsentence)
        
        sentences = re.split('[.,:]', line)
        sentences[0] = sentences[0].lstrip('[')
        sentences[0] = "(__-----)" + sentences[0] + "(__-----)"
        sentences[1] = sentences[1].rstrip(']\n')
        sentences[1] = "(__-----)" + sentences[1] + "(__-----)"
        listoflines.extend(sentences)
    elif '[Show text:' in line:
        
        rawsentence = re.split('"', rawline)
        rawfirstQuote = re.split('"', rawsentence[1])[0]
        
        
        sentences = re.split('"', line)[1]
        firstQuote = re.split('"', sentences)[0]
        if firstQuote != '' and (firstQuote not in lines[pos+2]):
            listoflines.append(firstQuote)
            listofrawlines.append(rawfirstQuote)
    elif '[' in line and ('image' in line or 'Image' in line):
        listofpromptlines.append(line)
    elif line[0] != '\n' and line[0] != '[':
        listoflines.append(line)
        listofrawlines.append(rawline)
        listofpromptlines.append(line)


with open(f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\PromptOutput.txt', 'w',encoding='utf-8') as file:
    for item in listofpromptlines:
        file.write("%s\n" % item)
        
        
with open(f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\voiceOutput.txt', 'w',encoding='utf-8') as file:
    for pos, item in enumerate(listofrawlines):
        try:
            if listofrawlines[pos+1][0] == '\"':
                item = item+'"'
                listofrawlines[pos+1] = listofrawlines[pos+1].lstrip('"')
        except:
            pass

        if item[0] == ' ':
            item = item.lstrip(' ')    
        if item[0] == '\n':
            item = item.lstrip('\n')
        print(bool(item),item,bool(item))
        
        if bool(item):
            wav = tts.tts(text=item,speaker=speaker, language="en", speed=1.08)
            # Text to speech to a file
            os.makedirs(f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\audio', exist_ok=True)
            tts.tts_to_file(text=item, speaker=speaker, language="en", file_path=f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\audio\\{pos} {speaker}_output.wav')
            file.write("%s\n" % item)

"""with open(f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}\\output.txt', 'w') as file:
    for item in listoflines:    
        if item[0] == '"':
                item = item.lstrip('"')
        if item[0] == ' ':
            item = item.lstrip(' ')    
        if item[0] == '\n':
            item = item.lstrip('\n')
        print(bool(item),item,bool(item))
        if bool(item):
            #makeGladosAudio(f'{scp}/Audio', item)
            file.write("%s\n" % item)
            
"""
