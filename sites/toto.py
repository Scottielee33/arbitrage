from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

def scrape_toto(driver):
    # Define a WebDriverWait instance with a 15-second timeout
    wait = WebDriverWait(driver, 10)

    # Open the specified webpage
    driver.get('https://sport.toto.nl/wedden/12/tennis/wedstrijden')

    # Wait for the accept cookies button to be clickable and click it
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accept-cookie-consent"]')))
    button.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.eventListEventHeaderCompetitionLevel-0-3-571')))
    check_elements = driver.find_elements(By.CSS_SELECTOR, '.eventListEventHeaderCompetitionLevel-0-3-571:nth-child(1)')

    check_element_texts = [element.text for element in check_elements]

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.loadMore-0-3-754')))
    load_more_buttons = driver.find_elements(By.CSS_SELECTOR, '.loadMore-0-3-754')
    for button in load_more_buttons[:-1]:
        button.click()
        time.sleep(0.1)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.eventListEventHeaderCompetitionLevel-0-3-571')))
    competition_elements = driver.find_elements(By.CSS_SELECTOR, '.eventListEventHeaderCompetitionLevel-0-3-571')
    for element in competition_elements:
        if element.text not in check_element_texts:
            ActionChains(driver).move_to_element(element).click(element).perform()
            time.sleep(0.1)

    # Wait for the elements to be present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class^="eventListItem"]')))

    # Select all elements with the class that starts with "eventListItem"
    elements = driver.find_elements(By.CSS_SELECTOR, '[class^="eventListItem"]')

    ls = []
    # Ensure elements are found
    if elements:
        # Loop through all matched elements and print their text
        for element in elements:
            lines = element.text.split('\n')
            if len(lines) > 8:
                ls.append(lines)
    else:
        print("No elements found with the specified class.")

    data = []
    ls = [i for n, i in enumerate(ls) if i not in ls[:n]]

    # Loop through the main list
    for sublist in ls:
        # Find the position of 'Winnaar' which precedes the odds
        try:
            pos_winnaar = sublist.index('Winnaar')
            pos1 = sublist[pos_winnaar:].index('1') + pos_winnaar
            pos2 = sublist[pos_winnaar:].index('2') + pos_winnaar
            # Extract the names and odds
            names = sublist[0:2]
            odds = [sublist[pos1 + 1], sublist[pos2 + 1]]

            for i in range(len(names)):
                if '/' in names[i]:
                    # It's a double game, so we extract the last names
                    split_names = names[i].split('/')
                    sorted_names = sorted([split_names[0].split()[0], split_names[1].split()[0]])
                    names[i] = ' & '.join(sorted_names)
                else:
                    if '.' in names[i]:
                        # If it's a dot-separated name, we take the second part as the last name
                        names[i] = names[i].split('.')[1].strip()
                    elif ',' in names[i]:
                        # If it's a comma-separated name, we take the first part as the last name
                        names[i] = names[i].split(',')[0].strip()
                    else:
                        # It's a single game, so we extract the last name
                        names[i] = names[i].split()[-1].strip()

            data.append(names + odds)
        except:
            pass

    # Convert the new list into a pandas DataFrame
    df_toto = pd.DataFrame(data, columns=['Name1', 'Name2', 'Odd1', 'Odd2'])
    # Replace commas with dots in the 'Odd1' and 'Odd2' columns
    df_toto['Odd1'] = df_toto['Odd1'].str.replace(',', '.')
    df_toto['Odd2'] = df_toto['Odd2'].str.replace(',', '.')

    # Convert the 'Odd1' and 'Odd2' columns to float
    df_toto['Odd1'] = df_toto['Odd1'].astype(float)
    df_toto['Odd2'] = df_toto['Odd2'].astype(float)

    # Remove duplicates
    df_toto = df_toto.drop_duplicates()
    df_toto['Match'] = df_toto[['Name1', 'Name2']].apply(lambda x: ' | '.join(sorted(x)), axis=1)
    df_toto[['Odd1', 'Odd2']] = df_toto.apply(lambda x: pd.Series([x['Odd2'], x['Odd1']] if x['Name1'] > x['Name2'] else [x['Odd1'], x['Odd2']]), axis=1)
    df_toto = df_toto.drop(['Name1', 'Name2'], axis=1)
    df_toto = df_toto.reindex(['Match', 'Odd1', 'Odd2'], axis=1)
    return df_toto

if __name__ == "__main__":
    driver = webdriver.Chrome()
    df = scrape_toto(driver)
    df.to_csv('toto.csv', index=False)
    print(df)