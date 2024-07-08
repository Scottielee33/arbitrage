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
        time.sleep(0.2)
        away_teams = driver.find_elements(By.CSS_SELECTOR, '.away_team')
        home_teams = driver.find_elements(By.CSS_SELECTOR, '.home_team')
        points2 = driver.find_elements(By.CSS_SELECTOR, '.point2')
        points1 = driver.find_elements(By.CSS_SELECTOR, '.point1')

        # Extract the text from the elements and append to the corresponding lists
        all_away_teams.extend([team.text for team in away_teams if team.text != ''])
        all_home_teams.extend([team.text for team in home_teams if team.text != ''])
        all_points2.extend([point.text for point in points2 if point.text != ''])
        all_points1.extend([point.text for point in points1 if point.text != ''])

    print(len(all_away_teams), len(all_home_teams), len(all_points2), len(all_points1))

    # Create a DataFrame
    df = pd.DataFrame({
        'Name1': all_home_teams,
        'Name2': all_away_teams,
        'Odd1': all_points1,
        'Odd2': all_points2
    })

    for row in df.itertuples():
        if '/' in row.Name1:
            split_names = row.Name1.split('/')
            sorted_names = sorted([split_names[0].split()[0], split_names[1].split()[0]])
            df.at[row.Index, 'Name1'] = ' & '.join(sorted_names)
        else:
            if '.' in row.Name1:
                df.at[row.Index, 'Name1'] = row.Name1.split(' ')[0].strip()
            else:
                df.at[row.Index, 'Name1'] = row.Name1.split(' ')[1].strip()
        if '/' in row.Name2:
            split_names = row.Name2.split('/')
            sorted_names = sorted([split_names[0].split()[0], split_names[1].split()[0]])
            df.at[row.Index, 'Name2'] = ' & '.join(sorted_names)
        else:
            if '.' in row.Name2:
                df.at[row.Index, 'Name2'] = row.Name2.split(' ')[0].strip()
            else:
                df.at[row.Index, 'Name2'] = row.Name2.split(' ')[1].strip()

    df['Match'] = df[['Name1', 'Name2']].apply(lambda x: ' | '.join(sorted(x)), axis=1)
    df[['Odd1', 'Odd2']] = df.apply(lambda x: pd.Series([x['Odd2'], x['Odd1']] if x['Name1'] > x['Name2'] else [x['Odd1'], x['Odd2']]), axis=1)
    df['Odd1'] = pd.to_numeric(df['Odd1'], errors='coerce')
    df['Odd2'] = pd.to_numeric(df['Odd2'], errors='coerce')
    df = df.reindex(['Match', 'Odd1', 'Odd2'], axis=1)
    return df

if __name__ == "__main__":
    driver = webdriver.Chrome()
    df = scrape_livebet(driver)
    print(df)