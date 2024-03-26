
from yahoo_driver import get_yahoo_driver, get_available_hitters, get_my_hitters
import pandas as pd
from unidecode import unidecode
import numpy as np


def build_available_hitters(available_hitters, my_ranks, razz_OPS, razz_100, gray_hitters, hitterlist, rotoballer):
    driver = get_yahoo_driver()

    df = pd.DataFrame(available_hitters, columns=['Player Name', 'Player Key'])
    df = df[df['Player Name'] != 'Max Muncy']
    df['My_ranks'] = df['Player Name'].map(my_ranks)
    df['Razz_OPS'] = df['Player Name'].map(razz_OPS)
    df['Gray'] = df['Player Name'].map(gray_hitters)
    df['HL'] = df['Player Name'].map(hitterlist)
    df['Razz_100'] = df['Player Name'].map(razz_100)
    df['Roto'] = df['Player Name'].map(rotoballer)
    df[['My_ranks', 'Razz_OPS', 'Gray', 'HL', 'Razz_100', 'Roto']] = df[['My_ranks', 'Razz_OPS', 'Gray', 'HL', 'Razz_100', 'Roto']].apply(pd.to_numeric, errors='coerce')
    
    columns = ['My_ranks', 'Razz_OPS', 'Gray', 'HL', 'Razz_100', 'Roto']
    weights = np.array([0.3, 0.3, 0.1, 0.1, 0.1, 0.1])
    
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
    df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\Available\available_hitters.csv', index=False)
    
    return None

def build_my_hitters(my_hitters, my_ranks, razz_OPS, razz_100, gray_hitters, hitterlist, rotoballer):
    driver = get_yahoo_driver()
    
    df = pd.DataFrame(my_hitters, columns=['Player Name', 'Player Key'])
    df['My_ranks'] = df['Player Name'].map(my_ranks)
    df['Razz_OPS'] = df['Player Name'].map(razz_OPS)
    df['Gray'] = df['Player Name'].map(gray_hitters)
    df['HL'] = df['Player Name'].map(hitterlist)
    df['Razz_100'] = df['Player Name'].map(razz_100)
    df['Roto'] = df['Player Name'].map(rotoballer)
    df[['My_ranks', 'Razz_OPS', 'Gray', 'HL', 'Razz_100', 'Roto']] = df[['My_ranks', 'Razz_OPS', 'Gray', 'HL', 'Razz_100', 'Roto']].apply(pd.to_numeric, errors='coerce')
    
    columns = ['My_ranks', 'Razz_OPS', 'Gray', 'HL', 'Razz_100', 'Roto']
    weights = np.array([0.3, 0.3, 0.1, 0.1, 0.1, 0.1])
    
    def weighted_average(row):
        if np.all(np.isnan(row)):
            return np.nan
        return np.average(row[~np.isnan(row)], weights=weights[~np.isnan(row)])

    df['Average'] = df[columns].apply(weighted_average, axis=1).round(1)
    df.dropna(subset=['Average'], inplace=True)
    df.sort_values(by='Average', ascending=True, inplace=True)
    df['%_Owned'] = df['Player Key'].apply(lambda x: driver.get_player_percent_owned_by_week(x).percent_owned_value)
    df.drop('Player Key', axis=1, inplace=True)
    df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\Available\my_hitters.csv', index=False)

    return None