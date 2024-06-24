from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import plotly.graph_objects as go
from dash import dcc
from player import Player

def display_graph(player_name): 
    try:
        player_id = players.find_players_by_full_name(player_name)[0]['id']
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24').get_data_frames()[0]
        player = Player(player_id, player_name)
        games = player.get_recent_games(game_log)

        fig = go.FigureWidget(
            data=[
                go.Bar(
                    name='Fantasy Points',
                    x=games['GAME_DATE'],
                    y=games['FAN_PTS'],
                    marker_color='#4D935D')
            ]
        )

        fig.add_trace(
            go.Scatter(
                mode='lines+markers',
                name='Minutes played',
                x=games['GAME_DATE'],
                y=games['MIN'],
                line=dict(color='pink'),
                marker=dict(color='red'))
        )

        previous_graph = dcc.Graph(
            id=player_name,
            figure=fig
        )
        return previous_graph

    except IndexError as e:
        logging.error(f"Player {player_name} not found: {e}")
        return html.Div(f"Player {player_name} not found.")
    except Exception as e:
        logging.error(f"Error fetching player data: {e}")
        return html.Div("An error occurred while fetching player data.")
