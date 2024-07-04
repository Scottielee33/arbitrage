from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import pandas as pd
from fuzzywuzzy import process

# Initialize the Firefox WebDriver
driver = webdriver.Firefox()

# Define a WebDriverWait instance with a 10-second timeout
wait = WebDriverWait(driver, 5)

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

df_unibet = pd.DataFrame(matches, columns=['Name1', 'Odd1', 'Name2', 'Odd2'])

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

# Save the unibet DataFrame to a CSV file
df_unibet.to_csv('unibet.csv', index=False)

# Save the toto DataFrame to a CSV file
df_toto.to_csv('toto.csv', index=False)

driver.quit()

# Load the data from the CSV files
df_unibet = pd.read_csv('unibet.csv')
df_toto = pd.read_csv('toto.csv')

# Define a function to match the names
def match_names(name, list_names, min_score=0):
    # -1 score incase we don't get any matches
    max_score = -1
    # Returning empty name for no match as well
    max_name = ""
    # Iternating over all names in the other
    for name2 in list_names:
        #Finding fuzzy match score
        score = process.extractOne(name, [name2], score_cutoff=min_score)
        # Checking if we are above our threshold and have a better score
        if score and score[1] > max_score:
            max_name = name2
            max_score = score[1]
    return max_name

# Create a list of unique names in the 'toto' DataFrame
names = df_toto[['Name1', 'Name2']].values.ravel()
unique_names = pd.unique(names)

# Apply the function to the 'unibet' DataFrame
df_unibet['Name1'] = df_unibet['Name1'].apply(lambda x: match_names(x, unique_names, 80))
df_unibet['Name2'] = df_unibet['Name2'].apply(lambda x: match_names(x, unique_names, 80))

# Merge the two DataFrames on the player names
df = pd.merge(df_unibet, df_toto, on=['Name1', 'Name2'], suffixes=('_unibet', '_toto'))

# Calculate the arbitrage opportunities
df['Arbitrage1'] = 1/df['Odd1_unibet'] + 1/df['Odd2_toto']
df['Arbitrage2'] = 1/df['Odd2_unibet'] + 1/df['Odd1_toto']

# Filter the DataFrame to only include rows where the arbitrage is less than 1
# df = df[df['Arbitrage'] < 1]

# Print the arbitrage opportunities
print(df)

# Save the DataFrame to a CSV file
df.to_csv('arbitrage.csv', index=False)