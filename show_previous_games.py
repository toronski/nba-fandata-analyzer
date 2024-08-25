from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import plotly.graph_objects as go
from dash import dcc
from player import Player
from queries import opponent_shorter

def display_graph(player_name, games_number): 
        player_id = players.find_players_by_full_name(player_name)[0]['id']
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24').get_data_frames()[0]
        player = Player(player_id, player_name)
        games = player.get_recent_games(game_log, games_number)
        print(games)
        games = games.iloc[::-1]
        games = opponent_shorter(games)
        games['MATCHUP_INDEXED'] = games['MATCHUP'] + ' (' + (games.index+1).astype(str) + ')'

        fig = go.FigureWidget(
            data=[
                go.Bar(
                    name='Fantasy Points',
                    x=games['MATCHUP_INDEXED'],
                    y=games['FAN_PTS'],
                    marker_color='#4D935D')
            ]
        )

        fig.add_trace(
            go.Scatter(
                mode='lines+markers',
                name='Minutes played',
                x=games['MATCHUP_INDEXED'],
                y=games['MIN'],
                line=dict(color='pink'),
                marker=dict(color='red'))
        )

        previous_graph = dcc.Graph(
            id=player_name,
            figure=fig
        )

        return previous_graph
