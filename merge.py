from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from fuzzywuzzy import process

from sites.toto import scrape_toto
from sites.unibet import scrape_unibet

def match_names(name, list_names, min_score=0):
    """
    Function to match the names using fuzzy matching.
    """
    max_score = -1
    max_name = ""
    for name2 in list_names:
        score = process.extractOne(name, [name2], score_cutoff=min_score)
        if score and score[1] > max_score:
            max_name = name2
            max_score = score[1]
    return max_name

def calculate_arbitrage():
    """
    Main function to scrape the data, match the names, calculate the arbitrage opportunities, and save the results.
    """
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    try:
        # Scrape the data
        df_toto = scrape_toto(driver)
        df_unibet = scrape_unibet(driver)
        df_toto.to_csv('toto.csv')
        df_unibet.to_csv('unibet.csv')
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
    finally:
        driver.quit()

    # Create a list of unique names in the 'toto' DataFrame
    unique_names = pd.unique(df_toto[['Name1', 'Name2']].values.ravel())

    # Apply the function to the 'unibet' DataFrame
    df_unibet['Name1'] = df_unibet['Name1'].apply(lambda x: match_names(x, unique_names, 80))
    df_unibet['Name2'] = df_unibet['Name2'].apply(lambda x: match_names(x, unique_names, 80))

    # Merge the two DataFrames on the player names
    df = pd.merge(df_unibet, df_toto, on=['Name1', 'Name2'], suffixes=('_unibet', '_toto'))

    # Calculate the arbitrage opportunities
    df['Arbitrage1'] = 1/df['Odd1_unibet'] + 1/df['Odd2_toto']
    df['Arbitrage2'] = 1/df['Odd2_unibet'] + 1/df['Odd1_toto']

    # Print the arbitrage opportunities
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('arbitrage.csv', index=False)

if __name__ == "__main__":
    calculate_arbitrage()