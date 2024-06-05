import time
import pickle
import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
def makeScript(driver):
    element = driver.find_element("xpath", "//*[contains(text(), 'Bees Swarm Containment Procedure')]")

    element.click()

def saveImage(driver):
    # Find all elements with a data-testid attribute
    elements = driver.find_element("xpath",'//*[@data-testid]')

    # Extract the numbers from the data-testid attributes
    numbers = [int(element.get_attribute('data-testid').replace('conversation-turn-', '')) for element in elements]

    # Find the largest number
    largest_number = max(numbers)

    # Find the element with the largest number in its data-testid attribute
    element = driver.find_element("xpath",f'//*[@data-testid="conversation-turn-{largest_number}"]')

    # Find the img tag with the specific class within the element
    img = element.ffind_element("css_selector", 'img.transition-opacity.duration-300.opacity-100')

    # Get the URL of the image
    img_url = img.get_attribute('src')

    # Download the image
    response = requests.get(img_url)

    # Save the image to a file
    with open(str(largest_number)+'_image.jpg', 'wb') as file:
        file.write(response.content)
    
def makeImage(driver):
    with open(r'C:\\Users\\Abdul\\Videos\\Youtube\\SCP_Channel\\013\\script.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        for i, line in enumerate(text.split('\n')):
            if i < 4:
                continue
            elif i//3 == 0:
                driver.find_element("id", "prompt-textarea").send_keys('\n' + line + Keys.RETURN)
                time.sleep(30)
                saveImage(driver)
            else:
                driver.find_element_by_id("prompt-textarea").send_keys( line+ '\n')


def givePrompt(driver):
    element = driver.find_element_by_id("prompt-textarea")
    element.click()
    element.send_keys("")



chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:\\Users\\Abdul\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=chrome_options)
#for selenium 4.15.2 options instead of chrome_options
#driver = webdriver.Chrome(options=chrome_options) 
driver.get("https://www.google.com/search?q=chatgpt")




time.sleep(5)

element=driver.find_element("xpath",'//a[@href="https://chat.openai.com/"]')

# Click on the element
element.click()
time.sleep(5)
input()