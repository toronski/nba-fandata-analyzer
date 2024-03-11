import queries as q
from dash import dcc
import plotly.graph_objects as go
import pandas as pd
from mysql_connector import engine


class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def show_previous_games(player_name):
        # get player info needed for 
        games = pd.read_sql_query(
            q.get_games_info(player_name), engine
        )
        games = games.tail(10) # in bracket value for number of showed games
        # built all matchup history
        fig = go.FigureWidget(
            data=[
                go.Bar(
                    name=player_name,
                    x=games['MATCHUP_DATE'],
                    y=games['FAN_PTS'],
                    marker_color='#4D935D')
            ]
        )

        # add minutes scatter
        fig.add_trace(
            go.Scatter(
                mode='lines+markers',
                name='Minutes played',
                x=games['MATCHUP_DATE'],
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
    
