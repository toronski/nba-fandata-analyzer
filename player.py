from queries import add_dd_and_td, fantasypts_counter

class Player:
    def __init__(self, player_id, player_name):
        self.player_id = player_id
        self.player_name = player_name

    def get_recent_games(self, game_log, num_games):
        print(num_games)
       
        games = game_log.head(num_games).copy()
        games = add_dd_and_td(games)
        games = fantasypts_counter(games)

        return games

    def get_attribute(self, attr):
        return getattr(self, attr, None)
