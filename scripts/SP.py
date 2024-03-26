from scripts.yahoo_driver import get_yahoo_driver, get_available_sp, get_my_SP
import pandas as pd
from unidecode import unidecode
import numpy as np

from scrapers.pl_scraper import get_pitcherlist
from scripts.scrapers.eno_scraper import get_eno_rankings
from scrapers.ss_scraper import get_ss_rankings
from scrapers.razz_scraper import get_gray_pitchers
from scrapers.roto_scraper import get_roto_pitchers


def build_available_sp(available_sp, gray_sp, pitcherlist, rotoballer, ss_ranks, eno_ranks):
    driver = get_yahoo_driver()
    
    df = pd.DataFrame(available_sp, columns=['Player Name', 'Player Key'])
    df['PL'] = df['Player Name'].map(pitcherlist)
    df['SS'] = df['Player Name'].map(ss_ranks)
    df['Gray'] = df['Player Name'].map(gray_sp)
    df['Eno'] = df['Player Name'].map(eno_ranks)
    df['Roto'] = df['Player Name'].map(rotoballer)
    df[['PL', 'SS', 'Gray', 'Eno', 'Roto']] = df[['PL', 'SS', 'Gray', 'Eno', 'Roto']].apply(pd.to_numeric, errors='coerce')
    
    columns = ['PL', 'SS', 'Gray', 'Eno', 'Roto']
    weights = np.array([0.4, 0.2, 0.133, 0.133, 0.133])
    
    def weighted_average(row):
        if np.all(np.isnan(row)):
            return np.nan
        return np.average(row[~np.isnan(row)], weights=weights[~np.isnan(row)])

    df['Average'] = df[columns].apply(weighted_average, axis=1).round(1)
    df.dropna(subset=['Average'], inplace=True)
    df.sort_values(by='Average', ascending=True, inplace=True)
    df = df.head(20)
    df['%_Owned'] = df['Player Key'].apply(lambda x: driver.get_player_percent_owned_by_week(x).percent_owned_value)
    df.drop('Player Key', axis=1, inplace=True)
    df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\Available\available_SP.csv', index=False)

    return None
    
def build_my_sp(my_sp, gray_sp, pitcherlist, rotoballer, ss_ranks, eno_ranks):
    driver = get_yahoo_driver()
    
    df = pd.DataFrame(my_sp, columns=['Player Name', 'Player Key'])
    df['PL'] = df['Player Name'].map(pitcherlist)
    df['SS'] = df['Player Name'].map(ss_ranks)
    df['Gray'] = df['Player Name'].map(gray_sp)
    df['Eno'] = df['Player Name'].map(eno_ranks)
    df['Roto'] = df['Player Name'].map(rotoballer)
    df[['PL', 'SS', 'Gray', 'Eno', 'Roto']] = df[['PL', 'SS', 'Gray', 'Eno', 'Roto']].apply(pd.to_numeric, errors='coerce')
    
    columns = ['PL', 'SS', 'Gray', 'Eno', 'Roto']
    weights = np.array([0.4, 0.2, 0.133, 0.133, 0.133])
    
    def weighted_average(row):
        if np.all(np.isnan(row)):
            return np.nan
        return np.average(row[~np.isnan(row)], weights=weights[~np.isnan(row)])

    df['Average'] = df[columns].apply(weighted_average, axis=1).round(1)
    df.dropna(subset=['Average'], inplace=True)
    df.sort_values(by='Average', ascending=True, inplace=True)
    df['%_Owned'] = df['Player Key'].apply(lambda x: driver.get_player_percent_owned_by_week(x).percent_owned_value)
    df.drop('Player Key', axis=1, inplace=True)
    df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\Available\my_SP.csv', index=False)
    
    return None