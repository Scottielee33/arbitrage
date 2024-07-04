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
driver.get('https://sport.toto.nl/wedden/12/tennis/wedstrijden')

# Wait for the accept cookies button to be clickable and click it
button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accept-cookie-consent"]')))
button.click()

# Wait for the page to load
time.sleep(1)

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
        if '/' not in names[0] and '/' not in names[1]:
            # Append the extracted data to the new list
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

print(df_toto)
driver.quit()