from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import schedule
import time
from multiprocessing import Process

from sites.toto import scrape_toto
from sites.unibet import scrape_unibet
from sites.livebet import scrape_livebet

def scrape_and_save(scrape_func, driver, filename):
    data = scrape_func(driver)
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    driver.quit()
    return df

def print_arbitrage_below_one(df):
    arbitrage_opps = df[(df['Arbitrage1'] < 1) | (df['Arbitrage2'] < 1)]
    arbitrage_opps.to_csv('arbitrage_below_one.csv', mode='a', header=False, index=False)
    print(arbitrage_opps)

def calculate_arbitrage():
    """
    Main function to scrape the data, match the names, calculate the arbitrage opportunities, and save the results.
    """
    with ThreadPoolExecutor() as executor:
        driver_toto = webdriver.Chrome()
        future_toto = executor.submit(scrape_and_save, scrape_toto, driver_toto, 'toto.csv')

        driver_livebet = webdriver.Chrome()
        future_livebet = executor.submit(scrape_and_save, scrape_livebet, driver_livebet, 'livebet.csv')

        driver_unibet = webdriver.Chrome()
        future_unibet = executor.submit(scrape_and_save, scrape_unibet, driver_unibet, 'unibet.csv')

    df_toto = future_toto.result()
    df_unibet = future_unibet.result()
    df_livebet = future_livebet.result()

    df_unibet_toto = pd.merge(df_unibet, df_toto, on=['Match'], suffixes=('_unibet', '_toto'))
    df_unibet_toto['Arbitrage1'] = 1 / df_unibet_toto['Odd1_unibet'] + 1 / df_unibet_toto['Odd2_toto']
    df_unibet_toto['Arbitrage2'] = 1 / df_unibet_toto['Odd2_unibet'] + 1 / df_unibet_toto['Odd1_toto']

    df_unibet_livebet = pd.merge(df_unibet, df_livebet, on=['Match'], suffixes=('_unibet', '_livebet'))
    df_unibet_livebet['Arbitrage1'] = 1 / df_unibet_livebet['Odd1_unibet'] + 1 / df_unibet_livebet['Odd2_livebet']
    df_unibet_livebet['Arbitrage2'] = 1 / df_unibet_livebet['Odd2_unibet'] + 1 / df_unibet_livebet['Odd1_livebet']

    df_toto_livebet = pd.merge(df_toto, df_livebet, on=['Match'], suffixes=('_toto', '_livebet'))
    df_toto_livebet['Arbitrage1'] = 1 / df_toto_livebet['Odd1_toto'] + 1 / df_toto_livebet['Odd2_livebet']
    df_toto_livebet['Arbitrage2'] = 1 / df_toto_livebet['Odd2_toto'] + 1 / df_toto_livebet['Odd1_livebet']

    print_arbitrage_below_one(df_unibet_toto)
    print_arbitrage_below_one(df_unibet_livebet)
    print_arbitrage_below_one(df_toto_livebet)
    df_unibet_toto.to_csv('arbitrage_unibet_toto.csv', index=False)
    df_unibet_livebet.to_csv('arbitrage_unibet_livebet.csv', index=False)
    df_toto_livebet.to_csv('arbitrage_toto_livebet.csv', index=False)

def run_scheduler():
    schedule.every(15).seconds.do(calculate_arbitrage)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=run_scheduler)
    p.start()
    p.join()