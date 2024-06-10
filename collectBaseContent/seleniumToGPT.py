#!/miniconda3/envs/imggen/python.exe 3.12.3
from ChatGPTAutomationHandler import ChatGPTAutomation
import os
from selenium.webdriver.common.keys import Keys
import os
import socket
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import requests
import sys
#sys.path.append('C:\\Users\\Abdul\\VSCODE_Projects\\Youtube-Generator\\Imgtovideo')
#from MakeSamples import StartAnimation

def selectGPTChatAndUsePrompt(chatgpt,gpt_chat,setup_prompt, text):
    input_box = chatgpt.driver.find_element(by=By.XPATH, value=f"//div[contains(text(), '{gpt_chat}')]")
    input_box.click()
    full_prompt = setup_prompt + text
    time.sleep(7)
    chatgpt.driver.find_element(By.ID, "prompt-textarea").send_keys(full_prompt)
    chatgpt.driver.find_element("id", "prompt-textarea").send_keys(Keys.ENTER)



def doSCPImgPromptFromURL(scpUrl,chatgpt,saveFolder):

    driver = webdriver.Chrome()
    driver.get(scpUrl)
    div_element = driver.find_element(By.ID,'page-content')
    # Get the text of the div element
    div_text = div_element.text
    # Split the text into lines
    lines = div_text.split('\n')
    # Get all lines except the first one and last 2
    lines_after_first = lines[1:]
    lines_before_end = lines_after_first[:-2]
    page = ''
    for i in lines_before_end:
        page = page + ' ' + i
    print(page)
    setup_prompt = "Turn This into a script of a man narrorating the document to a director, the narrorator  discuss tests that were ran and tests to run. Feel free to take creative liberties, be creative and feel free to add things you think would enrich the narrative of a man obsessed with tests that push the limits of understanding:"
    selectGPTChatAndUsePrompt(chatgpt,'Bees Swarm Containment Procedure',setup_prompt, page)
    time.sleep(66)
    
    
    resp = chatgpt.return_last_response_element()
    respneeded = resp.text
    # Split the text into lines
    lines = respneeded.split('\n')
    lines_after_first = lines[1:]
    lines_before_end = lines_after_first[:-2]
    # Join the lines back into a single string
    script = ''
    setup_prompt = r"Hello ChatGPT, I have a story script that I'd like to convert into prompts for generating images with DALL-E. The goal is to extract vivid, action-packed scenes that would make for visually compelling images. Please provide detailed prompts describing these actions without summarizing the chunks of text, Keep the number of people in the scene to a minimum, and keep the scene one instances in time, no transitions. The image should be ideal for AI animation from a single frame. Replace the SCP-### with a descriptive name that works better for image generation  Here is the text:"

    with open(saveFolder+'\\script.txt', 'w',encoding='utf-8') as file:
        for i in lines_before_end:
            file.write(i + '\n')
            script = script + ' ' + i
    selectGPTChatAndUsePrompt(chatgpt,'Image Prompts for DALL-E',setup_prompt, script)



def collectIMGPromptsActions(chatgpt,prompts):
    resp = chatgpt.return_last_response_element()
    respneeded = resp.text
    # Split the text into lines
    lines = respneeded.split('\n')
    
    # Get all lines except the first one
    lines_after_first = lines[1:]
    for i in lines_after_first:
        if len(i) > 200:
            prompts.append(i)
    # Join the lines back into a single string
    print(prompts)
    return prompts
    

def collectIMGPrompts(chatgpt):
    prompts = []
    prompts = collectIMGPromptsActions(chatgpt,prompts)
    chatgpt.driver.find_element("id", "prompt-textarea").send_keys("make me more prompts")
    time.sleep(3)
    chatgpt.driver.find_element("id", "prompt-textarea").send_keys(Keys.ENTER)
    time.sleep(90)
    prompts = collectIMGPromptsActions(chatgpt,prompts)
    return prompts


    
# Define the path where the chrome driver is installed on your computer
chrome_driver_path = r"C:\Users\Abdul\chromedriver.exe"

# the sintax r'"..."' is required because the space in "Program Files" in the chrome path
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
scp='002'
# Create an instance
chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)
projectFolder= f'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\{scp}'
os.makedirs(projectFolder+'\\photos', exist_ok=True)
driver = chatgpt.driver


doSCPImgPromptFromURL(f'https://scp-wiki.wikidot.com/scp-{scp}',chatgpt,projectFolder)
time.sleep(30)
promptList= collectIMGPrompts(chatgpt)

clickme= chatgpt.driver.find_element(by=By.XPATH, value=f"//div[contains(text(), 'Dalle Photos for Animations')]")
time.sleep(10)
clickme.click()
time.sleep(10)

chatgpt.makeImageFromList(projectFolder,promptList)

chatgpt.quit()
