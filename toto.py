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

print(ls)
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

# Remove duplicates
df_toto = df_toto.drop_duplicates()

print(df_toto)


# Convert the new list into a pandas DataFrame
df = pd.DataFrame(data, columns=['Name1', 'Name2', 'Odd1', 'Odd2'])

print(df)

# Close the WebDriver
driver.quit()

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
elements = driver.find_elements(By.CSS_SELECTOR, '.c539a')

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._8e013')))
scores = driver.find_elements(By.CSS_SELECTOR, '._8e013')

data = []

# Iterate over the names and scores in steps of 2
for i in range(0, len(elements), 2):
    # Get the names of the two players
    player1 = elements[i].text
    player2 = elements[i+1].text

    # Convert names from "Lastname, Firstname" to "Firstname Lastname"
    player1 = ' '.join(player1.split(', ')[::-1])
    player2 = ' '.join(player2.split(', ')[::-1])

    # Exclude the names that include a '/'
    if '/' in player1 or '/' in player2:
        continue

    # Get the odds for the two players
    odds1 = scores[i].text
    odds2 = scores[i+1].text

    # Append the data to the list
    data.append([player1, player2, odds1, odds2])

# Convert the list into a pandas DataFrame
df_unibet = pd.DataFrame(data, columns=['Player1', 'Player2', 'Odds1', 'Odds2'])

# Remove duplicates
df_unibet = df_unibet.drop_duplicates()

print(df_unibet)

driver.quit()

# Save the df_toto DataFrame to a CSV file
df_toto.to_csv('df_toto.csv', index=False)

# Save the df_unibet DataFrame to a CSV file
df_unibet.to_csv('df_unibet.csv', index=False)