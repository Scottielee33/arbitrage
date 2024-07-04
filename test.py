from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd

def get_data(driver, url, player_css, odds_css, button_xpath=None):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    if button_xpath:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        button.click()
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, player_css)))
    scores = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, odds_css)))
    data = []
    for i in range(0, len(elements), 2):
        player1 = ' '.join(elements[i].text.split(', ')[::-1])
        player2 = ' '.join(elements[i+1].text.split(', ')[::-1])
        if '/' in player1 or '/' in player2:
            continue
        odds1 = scores[i].text
        odds2 = scores[i+1].text
        data.append([player1, player2, odds1, odds2])
    return pd.DataFrame(data, columns=['Player1', 'Player2', 'Odds1', 'Odds2']).drop_duplicates()

with webdriver.Firefox() as driver:
    df_toto = get_data(driver, 'https://sport.toto.nl/wedden/12/tennis/wedstrijden', '[class^="eventListItem"]', '[class^="eventListItem"]', '//*[@id="accept-cookie-consent"]')
    df_unibet = get_data(driver, 'https://www.unibet.nl/betting/sports/filter/tennis/all/matches', '.c539a', '._8e013')

df_toto.to_csv('df_toto.csv', index=False)
df_unibet.to_csv('df_unibet.csv', index=False)