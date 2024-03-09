import pandas as pd
import sqlalchemy
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from functools import wraps
from configparser import ConfigParser
import time
import queries as q

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

# Save game logs of each player based on ID and Name into database
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
    # iterate through players list and save to database
    save_to_sql_log = 0
    for i, player_name in enumerate(players_list):
        player_data = players_data[player_name]
        player_data = player_data.iloc[::-1]
        player_data.to_sql(player_name, con=engine, index=False, if_exists='replace')

        # add double-double and triple-double columns
        alter_dd_query = q.alter_table(player_name, 'DD', 'INT')
        alter_td_query = q.alter_table(player_name, 'TD', 'INT')
        alter_fantasypts_query = q.alter_table(player_name, 'FAN_PTS', 'DECIMAL(5, 2)')
        
        # calculate dd and td
        update_dd_query = q.double_double_counter(player_name)
        update_td_query = q.triple_double_counter(player_name)
        update_fantasypts_query = q.fantasypts_counter(player_name)

        # save queries to database
        queries = (
            alter_dd_query, 
            update_dd_query, 
            alter_td_query, 
            update_td_query, 
            alter_fantasypts_query, 
            update_fantasypts_query)
        
        with engine.begin() as connection:
            for query in queries:
                connection.execute(query)
        
        
        save_to_sql_log += 1
        print(f"Done: {save_to_sql_log}, Name: {players_list[i]}")
    print('Saving players data complete')


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
def get_players_ids(arg):
    #players_index= sqlalchemy.Table('players_index', sqlalchemy.MetaData(), autoload_with=engine)
    result = pd.read_sql_query(q.get_all_players(), engine)
    ids_list = result['id'].tolist()
    names_list = result['full_name'].tolist()
    if arg == 'id':
        return ids_list
    elif arg == 'name':
        return names_list
    elif arg == 'id, name':
        return ids_list, names_list

# ids_list, names_list = get_players_ids()
# save_games_log(ids_list, names_list)



def test_case():
    ids = get_players_ids('name')
    print(ids)
    print(type(ids))
    print("Gotowe")

test_case()
