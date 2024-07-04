from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()  # or webdriver.Chrome(), depending on your browser
wait = WebDriverWait(driver, 10)

driver.get('https://www.bet365.com/')  # replace with the URL of your page

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.wn-PreMatchItem:nth-child(37)')))
button.click()