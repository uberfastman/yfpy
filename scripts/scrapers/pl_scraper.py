from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
from unidecode import unidecode


def get_pitcherlist(url: str):
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
    tables = driver.find_elements(By.TAG_NAME, "table")

    # Extract data from the table
    pitchers = []
    pattern = r'\nT\d*'
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        if len(rows) > 90:
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                for col in cols:
                    if len(col.text) > 4:
                        name = re.sub(pattern, '', col.text)
                        pitchers.append(name)   

    pitchers = {unidecode(pitcher).replace('.',''): idx+1 for idx, pitcher in enumerate(pitchers)}    

    # Close the driver
    driver.quit()
    return pitchers


def get_hitterlist(url: str):
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
    tables = driver.find_elements(By.TAG_NAME, "table")

    # Extract data from the table
    hitters = []
    pattern = r'\nT\d*'
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        if len(rows) > 90:
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                for col in cols:
                    if len(col.text) > 4:
                        name = re.sub(pattern, '', col.text)
                        hitters.append(name)   

    hitters = {unidecode(hitter).replace('.',''): idx+1 for idx, hitter in enumerate(hitters)}    

    # Close the driver
    driver.quit()
    return hitters


def get_hold_up(url: str):
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
    tables = driver.find_elements(By.TAG_NAME, "table")

    # Extract data from the table
    rp = []
    pattern = r'\nT\d*'
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        if len(rows) > 90:
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                for col in cols:
                    if len(col.text) > 4:
                        name = re.sub(pattern, '', col.text)
                        rp.append(name)   

    rp = {unidecode(rp).replace('.',''): idx+1 for idx, rp in enumerate(rp)}    

    # Close the driver
    driver.quit()
    return rp