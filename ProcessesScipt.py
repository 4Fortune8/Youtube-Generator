import re 
from glados_tts_main.glados import makeGladosAudio


replacements = {
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "Mrs.": "Missus",
    "(In a calm, robotic tone)": "",
    "Welcome, test subjects": "Welcome, Site Director",
    '.':'  !(-----) .', # it seems | deletes last word 
    ':':'  !(-----) :',
    "%": " percent",
    # Add more replacements as needed
}

def replace_all(text, dic):
    for old, new in dic.items():
        text = text.replace(old, new)
    return text

listoflines = []
 
scp = '008' 
 
with open(f'C:\\Users\Abdul\\Videos\\Youtube\\SCP Channel\\{scp}\\script.txt', 'r') as file:
    lines = file.readlines()
    
    
for pos, line in enumerate(lines):
    line= replace_all(line, replacements)     
    if 'GLaDOS' in line and line[0] != '[':
        line = line.split(':', 1)[1]
        sentences = re.split('[,.:]', line)
        listoflines.extend(sentences)
    elif '[Test Proposal' in line:
        sentences = re.split('[.,:]', line)
        sentences[0] = sentences[0].lstrip('[')
        sentences[0] = "(__-----)" + sentences[0] + "(__-----)"
        sentences[1] = sentences[1].rstrip(']\n')
        sentences[1] = "(__-----)" + sentences[1] + "(__-----)"
        listoflines.extend(sentences)
    elif '[Show text:' in line:
        sentences = re.split('"', line)[1]
        firstQuote = re.split('"', sentences)[0]
        if firstQuote != '' and (firstQuote not in lines[pos+2]):
            listoflines.append(firstQuote)


with open(f'C:\\Users\Abdul\\Videos\\Youtube\\SCP Channel\\{scp}\\output.txt', 'w') as file:
    for item in listoflines:
        
        if item[0] == '"':
                item = item.lstrip('"')
        if item[0] == ' ':
            item = item.lstrip(' ')    
        if item[0] == '\n':
            item = item.lstrip('\n')
        print(bool(item),item,bool(item))
        if bool(item):
            makeGladosAudio(f'{scp}/Audio', item)
            file.write("%s\n" % item)
            

