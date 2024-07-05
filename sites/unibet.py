from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Iterate over the elements
def flip_name(name):
    parts = name.split(',')
    parts = [part.strip() for part in parts]  # Remove leading/trailing whitespace
    return ' '.join(reversed(parts))

def scrape_unibet(driver):
    # Define a WebDriverWait instance with a 10-second timeout
    wait = WebDriverWait(driver, 10)

    # Open the specified webpage
    driver.get('https://www.unibet.nl/betting/sports/filter/tennis/all/matches')

    # Wait for at least one element with the class 'c539a' to be present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.c539a')))

    # Find all elements with class 'c539a'
    elements = driver.find_elements(By.CSS_SELECTOR, '._57b37+ ._6dae4 ._8e013 , .c539a')

    # Initialize an empty list to store the matches
    matches = []

    # Initialize variables to store the current match data
    player1 = player2 = odd1 = odd2 = None

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
                    player1 = flip_name(text)
                else:
                    player2 = flip_name(text)
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

    df = pd.DataFrame(matches, columns=['Name1', 'Odd1', 'Name2', 'Odd2'])
    return df