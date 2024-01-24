# data frame to mysql

import players_data
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from functools import wraps
import time

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

 
# Połączenie z bazą MySql
'''
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='lakmunsen115',
    db='players',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
'''


engine = create_engine('mysql+pymysql://root:lakmunsen115@localhost/players')

# Przykładowa lista graczy
example_players_list = ["Brandin Podziemski"]

# Konwertuj dict do dataframe
# player_dataframe = pd.DataFrame.from_dict(players_data.games_log(players_data.players_id(players_list), players_list))

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

print("Gotowe")
