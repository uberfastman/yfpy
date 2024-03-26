# %%
import pandas as pd
from unidecode import unidecode

# %%
the_list = get_the_list("https://pitcherlist.com/top-100-starting-pitchers-for-2024-fantasy-baseball-3-11-update/")

# %%
eno_rankings = get_eno_rankings()

# %%
razz_rankings = get_razzball_standard()

# %%
razz_qs = get_razzball_qs()

# %%
ss_rankings = get_ss_rankings()
# %%
##############SCRATCH##############
# Manual query
league_player_count = 0
league_player_retrieval_limit = 25
is_retry = False
players = yahoo_query.query(
                    f"https://fantasysports.yahooapis.com/fantasy/v2/league/431.l.6636/players;start=0;count=25status=A;position=2B;"
                    f"start={league_player_count};count={league_player_retrieval_limit if not is_retry else 1}",
                    ["league", "players"]
                )



# %%
available = dict()
for player in available_sp:
    if player.full_name in the_list.keys():
        available[the_list[player.full_name]] = player.full_name
# %%
sorted_list = sorted(available.items())
sorted_list

# %%
pitchers = []
for player in available_sp:
    pitchers.append(player.full_name)
    
    
# %%
hitters = []
for player in available_hitters:
    # print(type(available_hitters[i]))
    if isinstance(player, dict):
        hitters.append(player["player"].full_name)
    else:
        hitters.append(player.full_name)

hitters = [unidecode(string) for string in hitters]
# %%
razz_rankings = {i: v for i, (_, v) in enumerate(razz_rankings.items(), start=1)}

# %%
df = pd.DataFrame(pitchers, columns=['Player Name'])

# %%
# %%
df['PL'] = df['Player Name'].map(the_list)
df['SS'] = df['Player Name'].map(ss_rankings)
df['Eno'] = df['Player Name'].map(eno_rankings)
df['Razz_QS'] = df['Player Name'].map(razz_qs)
# df['Razz_QS'] = df['Player Name'].map(dict5)
# %%
df[['PL', 'SS', 'Eno', 'Razz_QS']] = df[['PL', 'SS', 'Eno', 'Razz_QS']].apply(pd.to_numeric, errors='coerce')
df['Average'] = df[['PL', 'SS', 'Eno', 'Razz_QS']].mean(axis=1)
# %%
df = df.sort_values('Average', ascending=True)
# %%
df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\my_yfpy\data\pitcherlist\hitters.csv', index=False)
# %%
razz_bats = get_razzball_standard()
# %%
razz_OPS = pd.read_csv(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\razz_OBP_SLG.csv", nrows=200)
hitterlist = pd.read_csv(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\hitterlist.csv")
my_ranks = pd.read_csv(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\my_ranks.csv")

# %%
df = pd.DataFrame(hitters, columns=['Player Name'])

# %%
df = df.merge(razz_OPS[['#', 'Name']], left_on='Player Name',right_on = 'Name',  how='left').rename(columns={'#': 'Razz_OPS'}).drop('Name', axis=1)
df = df.merge(hitterlist[['#', 'Name']], left_on='Player Name',right_on = 'Name',  how='left').rename(columns={'#': 'hitterlist'}).drop('Name', axis=1)
df = df.merge(my_ranks[['#', 'Name']], left_on='Player Name',right_on = 'Name',  how='left').rename(columns={'#': 'my_ranks'}).drop('Name', axis=1)

# %%
df['Razz'] = df['Player Name'].map(razz_bats)

# %%
df[['Razz_OPS', 'hitterlist', 'my_ranks', 'Razz']] = df[['Razz_OPS', 'hitterlist', 'my_ranks', 'Razz']].apply(pd.to_numeric, errors='coerce')

# %%
df['Average'] = df[['Razz_OPS', 'hitterlist', 'my_ranks', 'Razz']].mean(axis=1)

# %%
df = df.dropna(subset=['Average'])
# %%
if 'Max Muncy' in hitters:
    print('String found')
else:
    print('String not found')
# %%
# %%
file_path = r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\razz_100_hitters.csv"
df = pd.read_csv(file_path, nrows=200)
# %%
