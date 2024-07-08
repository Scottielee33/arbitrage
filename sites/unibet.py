from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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

    # Wait for the button with the specified CSS selector to be present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._0175e')))

    # Find all buttons with the specified CSS selector
    buttons_type = driver.find_elements(By.CSS_SELECTOR, '._0175e')
    buttons_type_text = [button.text for button in buttons_type]

    # Skip the first 4 buttons and click each of the rest
    for button in buttons_type[2:]:
        button.click()

    buttons_tournament = driver.find_elements(By.CSS_SELECTOR, '.fd7df')

    skip_next = False
    for button in buttons_tournament[4:]:
        # Get the button name
        button_name = button.text

        # If the button name is in `button_type`, set the flag to skip the next button
        if button_name in buttons_type_text:
            skip_next = True
        # If the flag is set, skip this button and unset the flag
        elif skip_next:
            skip_next = False
        # Otherwise, click the button
        else:
            ActionChains(driver).move_to_element(button).click(button).perform()

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
                    if '/' in text:
                        # It's a double game, so we extract the last names
                        names = text.split('/')
                        players = [names[0].split(', ')[0], names[1].split(', ')[0]]
                        players.sort()
                        player1 = ' & '.join(players)
                    else:
                        name = text.split(', ')[0]
                        player1 = name.split()[-1] if len(name.split()) > 1 else name
                else:
                    if '/' in text:
                        # It's a double game, so we extract the last names
                        names = text.split('/')
                        players = [names[0].split(', ')[0], names[1].split(', ')[0]]
                        players.sort()
                        player2 = ' & '.join(players)
                    else:
                        names = text.split(', ')
                        names.sort()
                        name = names[0]
                        player2 = name.split()[-1] if len(name.split()) > 1 else name
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
    df = df.drop_duplicates()
    df['Match'] = df[['Name1', 'Name2']].apply(lambda x: ' | '.join(sorted(x)), axis=1)
    df[['Odd1', 'Odd2']] = df.apply(lambda x: pd.Series([x['Odd2'], x['Odd1']] if x['Name1'] > x['Name2'] else [x['Odd1'], x['Odd2']]), axis=1)
    df = df.reindex(['Match', 'Odd1', 'Odd2'], axis=1)
    return df

if __name__ == "__main__":
    driver = webdriver.Chrome()
    df = scrape_unibet(driver)
    print(df)