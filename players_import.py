from nba_api.stats.static import players

def players_id(players_list)
    #initialize empty lists that will put player id into
    player_ids = [players.find_players_by_full_name(i)[0]['id'] for i in players_list]

    return player_ids
