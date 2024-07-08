from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from fuzzywuzzy import process
import concurrent.futures

from sites.toto import scrape_toto
from sites.unibet import scrape_unibet
from sites.livebet import scrape_livebet

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

def scrape_data(scrape_func, driver):
    try:
        return scrape_func(driver)
    except Exception as e:
        print(f"An error occurred while scraping with {scrape_func.__name__}: {e}")
    finally:
        driver.quit()

def print_arbitrage_below_one(df):
    df_below_one = df[(df['Arbitrage1'] < 1) | (df['Arbitrage2'] < 1)]
    if not df_below_one.empty:
        print(df_below_one)

def calculate_arbitrage():
    """
    Main function to scrape the data, match the names, calculate the arbitrage opportunities, and save the results.
    """
    drivers = [webdriver.Chrome() for _ in range(3)]
    scrape_funcs = [scrape_toto, scrape_unibet, scrape_livebet]

    # Scrape the data
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_data, func, driver) for func, driver in zip(scrape_funcs, drivers)]
        results = [future.result() for future in futures]

    df_toto, df_unibet, df_livebet = results

    df_unibet['Name1'] = df_unibet['Name1'].apply(lambda x: match_names(x, df_toto['Name1'].tolist()))
    df_unibet['Name2'] = df_unibet['Name2'].apply(lambda x: match_names(x, df_toto['Name2'].tolist()))

    df_livebet['Name1'] = df_livebet['Name1'].apply(lambda x: match_names(x, df_toto['Name1'].tolist()))
    df_livebet['Name2'] = df_livebet['Name2'].apply(lambda x: match_names(x, df_toto['Name2'].tolist()))
    # Merge the DataFrames on the player names and calculate the arbitrage opportunities
    df_unibet_toto = pd.merge(df_unibet, df_toto, on=['Name1', 'Name2'], suffixes=('_unibet', '_toto'))

    df_unibet_livebet = pd.merge(df_unibet, df_livebet, on=['Name1', 'Name2'], suffixes=('_unibet', '_livebet'))

    df_toto_livebet = pd.merge(df_toto, df_livebet, on=['Name1', 'Name2'], suffixes=('_toto', '_livebet'))

    # Convert columns to numeric type
    for df in [df_unibet_toto, df_unibet_livebet, df_toto_livebet]:
        for col in ['Odd1_unibet', 'Odd2_toto', 'Odd2_unibet', 'Odd1_toto', 'Odd1_livebet', 'Odd2_livebet']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Perform the division operation
    df_unibet_toto['Arbitrage1'] = 1/df_unibet_toto['Odd1_unibet'] + 1/df_unibet_toto['Odd2_toto']
    df_unibet_toto['Arbitrage2'] = 1/df_unibet_toto['Odd2_unibet'] + 1/df_unibet_toto['Odd1_toto']

    print_arbitrage_below_one(df_unibet_toto)

    df_unibet_livebet['Arbitrage1'] = 1/df_unibet_livebet['Odd1_unibet'] + 1/df_unibet_livebet['Odd2_livebet']
    df_unibet_livebet['Arbitrage2'] = 1/df_unibet_livebet['Odd2_unibet'] + 1/df_unibet_livebet['Odd1_livebet']

    print_arbitrage_below_one(df_unibet_livebet)

    df_toto_livebet['Arbitrage1'] = 1/df_toto_livebet['Odd1_toto'] + 1/df_toto_livebet['Odd2_livebet']
    df_toto_livebet['Arbitrage2'] = 1/df_toto_livebet['Odd2_toto'] + 1/df_toto_livebet['Odd1_livebet']

    print_arbitrage_below_one(df_toto_livebet)

    # Save the DataFrames to CSV files
    df_unibet_toto.to_csv('arbitrage_unibet_toto.csv', index=False)
    df_unibet_livebet.to_csv('arbitrage_unibet_livebet.csv', index=False)
    df_toto_livebet.to_csv('arbitrage_toto_livebet.csv', index=False)

if __name__ == "__main__":
    calculate_arbitrage()