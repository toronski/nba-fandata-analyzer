from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import plotly.graph_objects as go
from dash import dcc
from queries import add_dd_and_td, fantasypts_counter

def display_graph(player_name): 
    # find player ID
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    # download game log of a player as DataFrame
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24').get_data_frames()[0]
    # get player info needed for 
    games = game_log.head(10).copy()

    # adding Double-Double and Triple-Double columns
    games = add_dd_and_td(games)

    games = fantasypts_counter(games)

    # built all matchup history
    fig = go.FigureWidget(
        data=[
            go.Bar(
                name='Fantasy Points',
                x=games['GAME_DATE'],
                y=games['FAN_PTS'],
                marker_color='#4D935D')
        ]
    )

    # add minutes scatter
    fig.add_trace(
        go.Scatter(
            mode='lines+markers',
            name='Minutes played',
            x=games['GAME_DATE'],
            y=games['MIN'],
            line=dict(color='pink'),
            marker=dict(color='red'))
)

    # display graph
    previous_graph = dcc.Graph(
                        id=player_name,
                        figure=fig
                    ),
    return previous_graph