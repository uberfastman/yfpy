from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
from unidecode import unidecode

def get_roto_hitters(url: str):
    # Set up Selenium WebDriver
    s=Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--log-level=OFF")

    driver = webdriver.Chrome(service=s, options=options)
    
    # Navigate to the webpage
    driver.get(url)

    # Locate all tables
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    tables = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
    
    # Extract data from the table
    hitters = []
    pattern = r'\nT\d*'
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:  # Ensure the row has at least four columns
                name = cols[3].text
                hitters.append(name)
    hitters = {unidecode(hitter).replace('.',''): idx+1 for idx, hitter in enumerate(hitters)}    

    # Close the driver
    driver.quit()
    return hitters


def get_roto_pitchers(url: str):
    # Set up Selenium WebDriver
    s=Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--log-level=OFF")

    driver = webdriver.Chrome(service=s, options=options)
    
    # Navigate to the webpage
    driver.get(url)

    # Locate all tables
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    tables = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
    
    # Extract data from the table
    pitchers = []
    pattern = r'\nT\d*'
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:  # Ensure the row has at least four columns
                name = cols[3].text
                pitchers.append(name)
    pitchers = {unidecode(pitcher).replace('.',''): idx+1 for idx, pitcher in enumerate(pitchers)}    

    # Close the driver
    driver.quit()
    return pitchers