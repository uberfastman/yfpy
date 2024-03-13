# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time

def get_the_list(url: str):
    # Set up Selenium WebDriver
    s=Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=s, options=options)

    # Navigate to the webpage
    # url = "https://pitcherlist.com/the-list-8-28-top-100-starting-pitchers-week-22-fantasy-baseball-2023/"
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

    pitchers = {pitcher: idx+1 for idx, pitcher in enumerate(pitchers)}    

    # Close the driver
    driver.quit()
    return pitchers


# # %%
# list = get_the_list('https://pitcherlist.com/top-400-starting-pitchers-for-fantasy-baseball-2024-1-20-sps/')
# # %%
# list = {key: value for key, value in list.items() if 'Tier' not in key}
# list = {key: idx+1 for idx, key in enumerate(list)}
# # %%
# df = pd.DataFrame.from_dict(list, orient='index', columns=['Rank'])

# # %%
# df.to_csv(f'C:/Users/patri/OneDrive/Fantasy Baseball/2024/yfpy/data/pitcherlist/preseason_list.csv', index=True)

# # %%
