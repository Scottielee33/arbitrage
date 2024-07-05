from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import pandas as pd

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Define a WebDriverWait instance with a 10-second timeout
wait = WebDriverWait(driver, 10)

# Open the specified webpage
driver.get('https://www.12bet247.com/m/index.php#/get-champs/8')

# Find the elements by their class names
away_teams = driver.find_elements(By.CSS_SELECTOR, '.away_team')
home_teams = driver.find_elements(By.CSS_SELECTOR, '.home_team')
points2 = driver.find_elements(By.CSS_SELECTOR, '.point2')
points1 = driver.find_elements(By.CSS_SELECTOR, '.point1')

# Extract the text from the elements
away_teams = [team.text for team in away_teams]
home_teams = [team.text for team in home_teams]
points2 = [point.text for point in points2]
points1 = [point.text for point in points1]

# Print the scraped data
print("Away Teams:", away_teams)
print("Home Teams:", home_teams)
print("Points 2:", points2)
print("Points 1:", points1)

driver.quit()

time.sleep(5)