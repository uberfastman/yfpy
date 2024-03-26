from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_ss_rankings():
    
    # Set up Chrome in headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=OFF")
    
    driver = webdriver.Chrome(options=options)

# Navigate to the web page
    url = 'https://forums.bettoringreen.com/index.php?/topic/6212-sp-ranks-the-pre-spring-training-top-150/'
    driver.get(url)

    # List of XPaths for the spans containing the rankings
    span_xpaths = [
        '/html/body/main/div/div/div[1]/div[4]/div[3]/form/article[1]/div[2]/div/div[2]/div[1]/p[8]/span',
        '/html/body/main/div/div/div[1]/div[4]/div[3]/form/article[1]/div[2]/div/div[2]/div[1]/p[9]/span'
    ]
    

    # Empty string to hold the combined text
    combined_text = ""

    # Iterate through the XPaths, appending the text to the combined string
    for xpath in span_xpaths:
        span = driver.find_element(By.XPATH, xpath)
        combined_text += span.text + "\n"  # Adding a newline character for separation

    # Clean up and close the browser
    driver.quit()

    
    rankings = combined_text.split('\n')
    extracted_rankings = {}
    for ranking in rankings:
        parts = ranking.split('. ', 1)
        if len(parts) > 1:
            rank = parts[0]
            name = parts[1].split('-', 1)[0].strip()
            if rank.isdigit() and name:  # Ensures both rank and name are non-empty
                extracted_rankings[name] = rank

    return extracted_rankings