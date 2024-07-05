from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium import webdriver


def scrape_livebet(driver):
    # Define a WebDriverWait instance with a 10-second timeout
    wait = WebDriverWait(driver, 10)

    # Open the specified webpage
    driver.get('https://www.12bet247.com/m/index.php#/get-champs/8')

    # Wait for the page to load after each click
    time.sleep(5)

    buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pregame-championship-selection')))

    all_away_teams = []
    all_home_teams = []
    all_points2 = []
    all_points1 = []

    # Click on each button
    for button in buttons:
        button.click()
        time.sleep(0.1)
        away_teams = driver.find_elements(By.CSS_SELECTOR, '.away_team')
        home_teams = driver.find_elements(By.CSS_SELECTOR, '.home_team')
        points2 = driver.find_elements(By.CSS_SELECTOR, '.point2')
        points1 = driver.find_elements(By.CSS_SELECTOR, '.point1')

        # Extract the text from the elements and append to the corresponding lists
        all_away_teams.extend([team.text for team in away_teams if team.text != ''])
        all_home_teams.extend([team.text for team in home_teams if team.text != ''])
        all_points2.extend([point.text for point in points2 if point.text != ''])
        all_points1.extend([point.text for point in points1 if point.text != ''])

    driver.quit()
    # Create a DataFrame
    df = pd.DataFrame({
        'Name1': all_home_teams,
        'Name2': all_away_teams,
        'Odd1': all_points1,
        'Odd2': all_points2
    })

    # Return the DataFrame
    return df

driver = webdriver.Chrome()
df = scrape_livebet(driver)
print(df)