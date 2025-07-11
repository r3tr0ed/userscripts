from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import re
from time import sleep
options = webdriver.ChromeOptions()
profile_path = "/Users/maheralmoussaly/Library/Application Support/Google/Chrome/Default"
# options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-data-dir={profile_path}")
extension_path = "/Users/maheralmoussaly/desktop/unhinged-auto/5.0.1_0.crx"
options.add_extension(extension_path)
options.add_argument("-auto-open-devtools-for-tabs")
parser = argparse.ArgumentParser(description="Process URL.")
parser.add_argument("url", help="URL to process")
args = parser.parse_args()
url = args.url
# init driver
driver = webdriver.Chrome(options=options)
driver.get(url)

# ANSI Escape codes
ITALIC = "\033[3m"
RESET = "\033[0m"
DARKEN = "\033[90m"
def replace_italic_darken(textmatch):
    return f"{ITALIC}{DARKEN}{textmatch.group(1)}{RESET}{RESET}"


def get_messages():
    # Define a regular expression pattern to match text enclosed within **
    pattern = r"\*(.*?)\*"
    # Wait for presence of elements with class name "message-bubble-content"
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "message-bubble-content")))

    # Extract text content from the elements
    content = [element.text for element in elements]
    if content:
        for text in content:
            text = re.sub(pattern, replace_italic_darken, text)
            print(text)
        print("\n")
    else:
        print("Content not found.")
        quit()
    return content;
#init get messages first
get_messages()


def send_message(message):
    textarea = driver.find_element(By.CLASS_NAME, "input-container")
    textarea.send_keys(message)
    textarea.send_keys(Keys.ENTER)

while True:
    user_message = input("Send a message..")
    send_message(user_message)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "message-bubble-content")))
    print(RESET)
    get_messages()


