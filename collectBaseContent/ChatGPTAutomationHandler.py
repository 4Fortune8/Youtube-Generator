import os
import socket
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import requests

class ChatGPTAutomation:

    def __init__(self, chrome_path, chrome_driver_path, url = r"https://chat.openai.com"):
        """
        This constructor automates the following steps:
        1. Open a Chrome browser with remote debugging enabled at a specified URL.
        2. Prompt the user to complete the log-in/registration/human verification, if required.
        3. Connect a Selenium WebDriver to the browser instance after human verification is completed.

        :param chrome_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        :param chrome_driver_path: file path to chromedriver.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        """
        self.imagenumb = 0
        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        url = url
        free_port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(free_port, url)
        self.wait_for_human_verification()
        self.driver = self.setup_webdriver(free_port)
        if url == r"https://chat.openai.com":
            self.cookie = self.get_cookie()

    @staticmethod
    def find_available_port():
        """ This function finds and returns an available port number on the local machine by creating a temporary
            socket, binding it to an ephemeral port, and then closing the socket. """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def launch_chrome_with_remote_debugging(self, port, url):
        """ Launches a new Chrome instance with remote debugging enabled on the specified port and navigates to the
            provided url """

        def open_chrome():
            chrome_cmd = f"{self.chrome_path} --remote-debugging-port={port} --user-data-dir=remote-profile {url}"
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()

    def setup_webdriver(self, port):
        """  Initializes a Selenium WebDriver instance, connected to an existing Chrome browser
             with remote debugging enabled on the specified port"""

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = self.chrome_driver_path
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def get_cookie(self):
        """
        Get chat.openai.com cookie from the running chrome instance.
        """
        cookies = self.driver.get_cookies()
        cookie = [elem for elem in cookies if elem["name"] == '__Secure-next-auth.session-token'][0]['value']
        return cookie

    def send_prompt_to_chatgpt(self, prompt):
        """ Sends a message to ChatGPT and waits for 20 seconds for the response """

        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@id, "prompt-textarea")]')
        self.driver.execute_script(f"arguments[0].value = '{prompt}';", input_box)
        input_box.send_keys(Keys.RETURN)
        input_box.submit()
        self.check_response_ended()

    def check_response_ended(self):
        """ Checks if ChatGPT response ended """
        start_time = time.time()
        while len(self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')[-1].find_elements(
                by=By.CSS_SELECTOR, value='button.text-token-text-tertiary')) < 1:
            time.sleep(0.5)
            # Exit the while loop after 60 seconds anyway
            if time.time() - start_time > 60:
                break
        time.sleep(1)  # the length should be =4, so it's better to wait a moment to be sure it's really finished

    def return_chatgpt_conversation(self):
        """
        :return: returns a list of items, even items are the submitted questions (prompts) and odd items are chatgpt response
        """

        return self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')

    def save_conversation(self, file_name):
        """
        It saves the full chatgpt conversation of the tab open in chrome into a text file, with the following format:
            prompt: ...
            response: ...
            delimiter
            prompt: ...
            response: ...

        :param file_name: name of the file where you want to save
        """

        directory_name = "conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        delimiter = "|^_^|"
        chatgpt_conversation = self.return_chatgpt_conversation()
        with open(os.path.join(directory_name, file_name), "a") as file:
            for i in range(0, len(chatgpt_conversation), 2):
                file.write(
                    f"prompt: {chatgpt_conversation[i].text}\nresponse: {chatgpt_conversation[i + 1].text}\n\n{delimiter}\n\n")

    def return_last_response(self):
        """ :return: the text of the last chatgpt response """

        response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
        return response_elements[-3].text
    
    
    def return_last_response_element(self):
        """ :return: the text of the last chatgpt response element"""

        response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
        return response_elements[-3]

    @staticmethod
    def wait_for_human_verification():
        print("You need to manually complete the log-in or the human verification if required.")
        print("REE")
        while True:
            user_input = input(
                "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower().strip()

            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)  # You can adjust the waiting time as needed
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def saveImage(self,folderPath):
        print("Saving the image...")
        # Find all elements with a data-testid attribute
        

        # Find the element with the largest number in its data-testid attribute
        element = self.return_last_response_element()
        # Find the img tag with the specific class within the element
        imgs = self.driver.find_elements(By.CSS_SELECTOR, 'img.transition-opacity.duration-300.opacity-100')
        img = imgs[-1]
        
        # Get the URL of the image
        img_url = img.get_attribute('src')

        # Download the image
        response = requests.get(img_url)

        # Save the image to a file
        with open(folderPath+"\\photos\\"+str(self.imagenumb)+'.png', 'wb') as file:
            file.write(response.content)
        self.imagenumb += 1
            
        
        
    def refreshPrompt(self):
        element = self.return_last_response_element()
        spans = self.driver.find_elements(By.CSS_SELECTOR, 'span:nth-child(3)')
        span = spans[-1]
        try:
            span.click()
        except:
            time.sleep(200)
        
        self.check_response_ended()
        
   
    def makeImageFromList(self, folderPath,list):
        import random
        driver = self.driver
        action = webdriver.ActionChains(driver)
        for prompt in list:
            print("makeImage")
            driver.find_element("id", "prompt-textarea").send_keys('make me a HD 1792x1024 image of the following:')
            driver.find_element("id", "prompt-textarea").send_keys( prompt + "\n")
            self.check_response_ended()
            time.sleep(random.randint(1, 5))
            self.saveImage(folderPath)
            print("saved")
            self.refreshPrompt()
            print("refreshed")
            self.saveImage(folderPath)
            print("saved")
            driver.find_element("id", "prompt-textarea").send_keys('make me a HD 1792x1024 image of the following:')
            action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(
            Keys.ENTER).key_up(Keys.SHIFT).perform()
    

        
    def makeImageFromFile(self, folderPath,scriptPath):
        driver = self.driver
        ImgeScripfilePath = scriptPath
        action = webdriver.ActionChains(driver)
        with open(ImgeScripfilePath, 'r', encoding='utf-8') as file:
            print("makeImage")
            driver.find_element("id", "prompt-textarea").send_keys('make me a HD 1792x1024 image of the following text:')
            text = file.read()
            for i, line in enumerate(text.split('\n')):
                if i < 4:
                    continue
                elif '[' in line:
                    driver.find_element("id", "prompt-textarea").send_keys( line + "\n")
                    self.check_response_ended()
                    self.saveImage(folderPath)
                    print("saved")
                    self.refreshPrompt()
                    print("refreshed")
                    self.saveImage(folderPath)
                    print("saved")
                    driver.find_element("id", "prompt-textarea").send_keys('make me a HD 1792x1024 image of the following text:')
                    action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(
                    Keys.ENTER).key_up(Keys.SHIFT).perform()
                else:
                    driver.find_element("id","prompt-textarea").send_keys( line )
                    
                    action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(
                    Keys.ENTER).key_up(Keys.SHIFT).perform()
                    print(i%3)
    
        
    def quit(self):
        """ Closes the browser and terminates the WebDriver session."""
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()
