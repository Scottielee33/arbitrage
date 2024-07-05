from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import pandas as pd

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Define a WebDriverWait instance with a 10-second timeout
wait = WebDriverWait(driver, 10)

# Open the specified webpage
driver.get('https://www.betnation.nl/sports#/tennis/upcoming/today/match12')

# Find the button element
buttons = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[4]/div[1]/div[2]/button[4]')

# Check if any buttons were found
if buttons:
    # Click the first button
    buttons[0].click()
else:
    print("No button found")

selector = 'mggcv2-pb-1.5 mggcv2-text-panel mggcv2-flex mggcv2-flex-col mggcv2-bg-popularLP-event mggcv2-border-b mggcv2-border-popularLP-event-borderBottom'

# Find elements with the specified class
elements = driver.find_elements(By.CLASS_NAME, ' '.join(selector.split()))
texts = []

# Loop through the elements and extract the text
for element in elements:
    texts.append(element.text)

# Print the texts
for text in texts:
    print(text)