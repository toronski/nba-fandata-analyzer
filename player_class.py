import queries as q
from dash import dcc
import plotly.graph_objects as go
import pandas as pd
from mysql_connector import engine


class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def show_previous_games(player_name):
        # get player info needed for 
        player = pd.read_sql_query(
            q.get_games_info(player_name), engine
        )
        player = player.tail(10) # in bracket value for number of showed games
        # built all matchup history
        fig = go.FigureWidget(
            data=[
                go.Bar(
                    name=player_name,
                    x=player['MATCHUP_DATE'],
                    y=player['FAN_PTS'],
                    marker_color='#4D935D')
            ]
        )

        # add minutes scatter
        fig.add_trace(
            go.Scatter(
                mode='lines+markers',
                name='Minutes played',
                x=player['MATCHUP_DATE'], y=player['MIN'],
                line=dict(color='pink'),
                marker=dict(color='red'))
)

        # display graph
        previous_graph = dcc.Graph(
                            id=player_name,
                            figure=fig
                        ),
        return previous_graph
    

    def 