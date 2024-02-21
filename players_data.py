import pandas as pd
import sqlalchemy
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from functools import wraps
from configparser import ConfigParser
import time

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}\nTook {total_time:.4f} seconds')
        return result
    return timeit_wrapper


# connect to mysql based on info found in config.ini
def connect_to_mysql():
    config = ConfigParser()
    config.read('config.ini')
    DB_USER = config.get('Database', 'DB_USER')
    DB_PASSWORD = config.get('Database', 'DB_PASSWORD')
    DB_HOST = config.get('Database', 'DB_HOST')
    #DB_PORT = config.get('Database', 'DB_PORT')
    DB_NAME = config.get('Database', 'DB_NAME')
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
    return engine


engine = connect_to_mysql()

# Pull game logs of each player based on ID and Name
@timeit
def save_games_log(players_ids, players_list):
    print('Starting save_games_log')
    # pull game logs of each player
    games_logs = []
    players_log = 0
    for i, id in enumerate(players_ids):
        game_log = playergamelog.PlayerGameLog(player_id=id, season=SeasonAll.default).get_data_frames()[0]
        games_logs.append(game_log)
        players_log += 1
        print(f"Done: {players_log} ID: {players_ids[i]}")
    print('Downloading players data complete')

    players_data = dict(zip(players_list, games_logs))

    print("Starting to iterate and save players.")
    # Iterate through players list and save to database
    save_to_sql_log = 0
    for i, player_name in enumerate(players_list):
        player_data = players_data[player_name]
        player_data = player_data.iloc[::-1]
        player_data.to_sql(player_name, con=engine, index=False, if_exists='replace')

        # add double-double and triple-double columns
        alter_dd_query = sqlalchemy.text(f"ALTER TABLE players.`{player_name}` ADD DD INT DEFAULT 0")
        alter_td_query = sqlalchemy.text(f"ALTER TABLE players.`{player_name}` ADD TD INT DEFAULT 0")
        
        # calculate dd and td
        update_dd_query = sqlalchemy.text(
            f"""UPDATE players.`{player_name}`
            SET DD = CASE
                WHEN (
                    (PTS >= 10) +
                    (REB >= 10) +
                    (AST >= 10) +
                    (STL >= 10) +
                    (BLK >= 10)
                ) >= 2 THEN 1
                ELSE 0
            END;"""
        )

        update_td_query = sqlalchemy.text(
            f"""UPDATE players.`{player_name}`
            SET TD = CASE
                WHEN (
                    (PTS >= 10) +
                    (REB >= 10) +
                    (AST >= 10) +
                    (STL >= 10) +
                    (BLK >= 10)
                ) >= 3 THEN 1
                ELSE 0
            END;"""
        )

        # save queries to database
        with engine.begin() as connection:
            connection.execute(alter_dd_query)
            connection.execute(update_dd_query)
            connection.execute(alter_td_query)
            connection.execute(update_td_query)
            
        save_to_sql_log += 1
        print(f"Done: {save_to_sql_log}, Name: {players_list[i]}")
    print('Saving players data complete')


def save_dd_td(player_name):
    pd.read_sql_query('SELECT id, full_name FROM players_index', engine)

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
    ids_list = result['id'].tolist()
    names_list = result['full_name'].tolist()
    return ids_list, names_list


# ids_list, names_list = get_players_ids()
# save_games_log(ids_list, names_list)



def test_case2():
    names_list = ['Brandin Podziemski', 'LeBron James', 'Nikola Jokic']
    ids_list = players_id(names_list)
    save_games_log(ids_list, names_list)
    print("Gotowe")

test_case2()

def test_case():
    example_players_list = ["Brandin Podziemski"]
    # Ściągnij informacje o graczu
    players_id_list = players_id(example_players_list)
    #print(f'Players ID list\n {players_id_list}')
    #print(type(players_id_list))

    # Zbierz game log graczy z listy
    players_game_log = save_games_log(players_id_list, example_players_list)
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
    print('gotowe')

# games_logs = [playergamelog.PlayerGameLog(player_id=i, season = SeasonAll.default).get_data_frames()[0] for i in players_ids]
