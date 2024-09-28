import plotly.graph_objects as go
from dash import dcc
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from player import Player
from queries import opponent_shorter

def graph_preparation(player_name, games_number, season, team_filter=None):
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
    player = Player(player_id, player_name)
    games = player.get_recent_games(game_log, games_number)
    games = games.iloc[::-1]
    games = opponent_shorter(games)

    if team_filter:
        games = games[games['MATCHUP'].str.contains(team_filter)]

    games['MATCHUP_INDEXED'] = games['MATCHUP'] + ' (' + (games.index+1).astype(str) + ')'
    
    return games


def previous_games_graph(player_name, games_number, season, team_filter=None): 
    games = graph_preparation(player_name, games_number,season, team_filter)

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
            marker=dict(color='red')
        )
    )

    fig.update_layout(
            autosize=True,
            minreducedwidth=250,
            minreducedheight=250,
            width=800,
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            # title={
            #     'text': "Previous games",
            #     'y':0.9,
            #     'x':0.22,
            #     'xanchor': 'right',
            #     'yanchor': 'top',
            #     'font': {
            #         'size': 18.5,
            #         'family': 'Arial, sans-serif'
            #     }
            # }
        )

    previous_graph = dcc.Graph(
        id=player_name,
        config={
            'displayModeBar': False,
            'displaylogo': False,
            'modeBarButtonsToRemove':
                ['resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian']
        },
        figure=fig,
        #config={'responsive': True},
        style={'width': '90%', 'height': '350px'}
    )

    return previous_graph


def one_previous_opponent(player_name, games_number, season, team_filter):
    games = graph_preparation(player_name, games_number, season, team_filter)

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
            marker=dict(color='red')
        )
    )

    fig.update_layout(
        autosize=False,
        minreducedwidth=250,
        minreducedheight=250,
        width=800,
        height=250,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    one_previous_opponent = dcc.Graph(
        id=player_name,
        figure=fig,
        config={
            'displayModeBar': False,
            'displaylogo': False,
            'modeBarButtonsToRemove':
                ['resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian']
        },
        style={'width': '90%', 'height': '350px'}
    )

    return one_previous_opponent