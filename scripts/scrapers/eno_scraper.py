import requests
from bs4 import BeautifulSoup

def get_eno_rankings():
    url = 'https://theathletic.com/5224402/2024/01/29/eno-sarris-starting-pitcher-fantasy-baseball-ranking/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rankings = soup.find_all('div', class_='fc-rank-text')
    players = soup.find_all('h3', class_='fc-player-headline')

    # Extract the text from each tag and pair them up
    ranked_players = {player.text: rank.text for player, rank in zip(players, rankings)}
    
    return ranked_players
