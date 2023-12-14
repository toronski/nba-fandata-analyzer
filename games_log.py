from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

def games_log(player_ids, players_list):
    #pull game logs of each player
    game_logs = [playergamelog.PlayerGameLog(player_id=i, season = SeasonAll.all).get_data_frames()[0] for i in player_ids]
    player_data = dict(zip(players_list, game_logs))

    return player_data


def players_id(players_list):
    #initialize empty lists that will put player id into
    player_ids = [players.find_players_by_full_name(i)[0]['id'] for i in players_list]

    return player_ids

players_list = ["Brandin Podziemski", "Victor Wembanyama"]

ids = players_id(players_list)
datas = games_log(ids, players_list)

print(datas["Brandin Podziemski"])

