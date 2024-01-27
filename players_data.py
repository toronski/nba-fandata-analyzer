import pandas as pd
from sqlalchemy import create_engine
from functools import wraps
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll



engine = create_engine('mysql+pymysql://root:lakmunsen115@localhost/players')

def games_log(player_ids, players_list):
    # pull game logs of each player
    game_logs = [playergamelog.PlayerGameLog(player_id=i, season = SeasonAll.all).get_data_frames()[0] for i in player_ids]
    player_data = dict(zip(players_list, game_logs))
    return player_data
    

def players_id(players_list):
    # initialize empty lists that will put player id into
    player_ids = [players.find_players_by_full_name(i)[0]['id']
                  for i in players_list]
    return player_ids


def get_players():
    # Create database of all active players
    get_players = players.get_active_players()
    all_players_df = pd.DataFrame(get_players)
    all_players_df.to_sql('players_index', con=engine, index=False, if_exists='replace')


get_players()
print("gotowe")

"""
Wywołaj listę wszystkich graczy.
Zapisz wszystkich graczy w bazie danych.
Wyciągnij ID wszystkich graczy z bazy danych i dodaj ich do listy.
Ściągnij statystyki wszystkich gracz z listy i dodaj je do bazy danych.



# Ściągnij informacje o graczu
players_id_list = players_data.players_id(example_players_list)
# print(players_id_list)
# print(type(players_id_list))

# Zbierz game log graczy z listy
players_game_log = players_data.games_log(players_id_list, example_players_list)

test_query_brandin = players_game_log["Brandin Podziemski"]
# print(type(test_query_brandin))

# Przyjmij, że masz DataFrame o nazwie 'df'
df = test_query_brandin

# Zmień 'table_name' na nazwę, którą chcesz przypisać tabeli w bazie danych
table_name = 'Brandin Podziemski'
df.to_sql(table_name, con=engine, index=False, if_exists='replace')


#players_list = ["Brandin Podziemski", "LeBron James"]
##ids = players_id(players_list)
#datas = games_log(ids, players_list)
#test_query = datas["Brandin Podziemski"]
# print(type(test_query))

"""