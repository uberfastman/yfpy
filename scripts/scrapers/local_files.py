import pandas as pd
from unidecode import unidecode

def get_local_file(file_path: str):
    df = pd.read_csv(file_path, nrows=200)
    df.sort_values('#', inplace=True)
    players = df['Name'].tolist()
    
    return {unidecode(player).replace('.',''): idx+1 for idx, player in enumerate(players)}

    
