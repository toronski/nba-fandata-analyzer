import pandas as pd
import sqlalchemy
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import mysql.connector as msc


engine = sqlalchemy.create_engine('mysql+pymysql://root:lakmunsen115@localhost/players')


# Pull game logs of each player based on ID and Name
def save_games_log(player_ids, players_list):
    # pull game logs of each player
    games_logs = [playergamelog.PlayerGameLog(player_id=i, season = SeasonAll.all).get_data_frames()[0] for i in player_ids]
    players_data = dict(zip(players_list, games_logs))
    # Iterate through players list and save to database
    for player_name in players_list:
        player_data = players_data[player_name]
        player_data = player_data.iloc[::-1]
        player_data.to_sql(player_name, con=engine, index=False, if_exists='replace')


# Find players names based on ID
def players_id(players_list):
    # initialize empty lists that will put player id into
    player_ids = [players.find_players_by_full_name(i)[0]['id']
                  for i in players_list]
    return player_ids


# Save players IDs and Names into database
def save_active_players():
    # Create database of all active players
    get_players = players.get_active_players()
    all_players_df = pd.DataFrame(get_players)
    all_players_df.to_sql('players_index', con=engine, index=False, if_exists='replace')


# Get players IDs and names from DB
def get_players_ids():
    #players_index= sqlalchemy.Table('players_index', sqlalchemy.MetaData(), autoload_with=engine)
    
    result = pd.read_sql_query('SELECT id, full_name FROM players_index', engine)
    print(result)



get_players_ids()
"""
print(id_list)
print(type(id_list))
print(name_list)
print(type(name_list))
Wywołaj listę wszystkich graczy.
Zapisz wszystkich graczy w bazie danych.
Wyciągnij ID wszystkich graczy z bazy danych i dodaj ich do listy.
Ściągnij statystyki wszystkich gracz z listy i dodaj je do bazy danych.

"""

"""


def test_case():
    example_players_list = ["Brandin Podziemski"]
    # Ściągnij informacje o graczu
    players_id_list = players_id(example_players_list)
    #print(f'Players ID list\n {players_id_list}')
    #print(type(players_id_list))

    # Zbierz game log graczy z listy
    players_game_log = games_log(players_id_list, example_players_list)
    #print(f'Players game log\n {players_game_log}')
    #print(type(players_game_log))
    test_query_brandin = players_game_log["Brandin Podziemski"]
    #print(f'Test query\n {test_query_brandin}')
    print(type(test_query_brandin))

    # Przyjmij, że masz DataFrame o nazwie 'df'
    df = test_query_brandin
    # Odwróć tego data frama
    df_reversed = df.iloc[::-1]
    
    
    print(f"Standardowa baza\n\n{df}")
    #print(type(df))
    print(f"Odwrócona baza\n\n{df_reversed}")


#test_case()
print('gotowe')



# Zmień 'table_name' na nazwę, którą chcesz przypisać tabeli w bazie danych
table_name = 'Brandin Podziemski'
df.to_sql(table_name, con=engine, index=False, if_exists='append')
'''


#players_list = ["Brandin Podziemski", "LeBron James"]
##ids = players_id(players_list)
#datas = games_log(ids, players_list)
#test_query = datas["Brandin Podziemski"]
# print(type(test_query))
"""
