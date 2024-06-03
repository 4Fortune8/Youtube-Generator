import time
import pickle
import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:\\Users\\Abdul\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=chrome_options)
#for selenium 4.15.2 options instead of chrome_options
#driver = webdriver.Chrome(options=chrome_options) 
driver.get("https://chatgpt.com/")


time.sleep(5)

element = driver.find_element("xpath", "//*[contains(text(), 'Bees Swarm Containment Procedure')]")
element.click()


input()