from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import pandas as pd

# Initialize the Firefox WebDriver
driver = webdriver.Firefox()

# Define a WebDriverWait instance with a 10-second timeout
wait = WebDriverWait(driver, 10)

# Open the specified webpage
driver.get('https://www.unibet.nl/betting/sports/filter/tennis/all/matches')

# Define a WebDriverWait instance with a 10-second timeout
wait = WebDriverWait(driver, 10)

# Wait for at least one element with the class 'c539a' to be present
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.c539a')))

# Find all elements with class 'c539a'
elements = driver.find_elements(By.CSS_SELECTOR, '._57b37+ ._6dae4 ._8e013 , .c539a')
data = []

# Iterate over the elements in steps of 4
i = 0
while i < len(elements):
    # Get the names of the two players
    player1 = elements[i].text
    player2 = elements[i+1].text

    # Convert names from "Lastname, Firstname" to "Firstname Lastname"
    player1 = ' '.join(player1.split(', ')[::-1])
    player2 = ' '.join(player2.split(', ')[::-1])

    # Exclude the names that include a '/'
    if '/' in player1 or '/' in player2:
        i += 2
        continue

    # Check if the third and fourth elements are odds
    try:
        odds1 = float(elements[i+2].text)
        odds2 = float(elements[i+3].text)
        i += 4
    except ValueError:
        # If they are not odds, skip this group and consider them as next players
        i += 2
        continue

    # Append the data to the list
    data.append([player1, player2, odds1, odds2])

print(data)