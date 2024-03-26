from yahoo_driver import get_yahoo_driver, get_available_rp, get_my_RP
from scrapers.pl_scraper import get_hold_up
import pandas as pd
from unidecode import unidecode
import numpy as np


def build_available_rp(available_rp, hold_up):
    driver = get_yahoo_driver()
    
    df = pd.DataFrame(available_rp, columns=['Player Name', 'Player Key'])
    df['HoldUp'] = df['Player Name'].map(hold_up)
    df['HoldUp'] = df['HoldUp'].apply(pd.to_numeric, errors='coerce')
    
    df.dropna(subset=['HoldUp'], inplace=True)
    df.sort_values(by='HoldUp', ascending=True, inplace=True)
    df = df.head(20)
    df['%_Owned'] = df['Player Key'].apply(lambda x: driver.get_player_percent_owned_by_week(x).percent_owned_value)
    df.drop('Player Key', axis=1, inplace=True)
    df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\Available\available_RP.csv', index=False)
    
    
def build_my_rp(my_rp, hold_up):
    driver = get_yahoo_driver()
    
    df = pd.DataFrame(my_rp, columns=['Player Name', 'Player Key'])
    df['HoldUp'] = df['Player Name'].map(hold_up)
    df['HoldUp'] = df['HoldUp'].apply(pd.to_numeric, errors='coerce')
    
    df.dropna(subset=['HoldUp'], inplace=True)
    df.sort_values(by='HoldUp', ascending=True, inplace=True)
    df = df.head(20)
    df['%_Owned'] = df['Player Key'].apply(lambda x: driver.get_player_percent_owned_by_week(x).percent_owned_value)
    df.drop('Player Key', axis=1, inplace=True)
    df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\Available\my_RP.csv', index=False)
