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

# Initialize an empty list to store the matches
matches = []

# Initialize variables to store the current match data
player1 = player2 = odd1 = odd2 = None

# Iterate over the elements
for element in elements:
    text = element.text

    # If we're expecting a player name
    if not player1 or not player2:
        # If the text can be converted to a float, it's an odd, so we skip this match
        try:
            float(text)
            player1 = player2 = odd1 = odd2 = None
        except ValueError:
            # If the text can't be converted to a float, it's a player name
            if not player1:
                player1 = text
            else:
                player2 = text
    # If we're expecting an odd
    else:
        # If the text can't be converted to a float, it's a player name, so we skip this match
        try:
            odd = float(text)
            if not odd1:
                odd1 = odd
            else:
                odd2 = odd
                matches.append((player1, odd1, player2, odd2))
                player1 = player2 = odd1 = odd2 = None
        except ValueError:
            player1 = player2 = odd1 = odd2 = None

df = pd.DataFrame(matches, columns=['Player 1', 'Odds 1', 'Player 2', 'Odds 2'])

driver.quit()