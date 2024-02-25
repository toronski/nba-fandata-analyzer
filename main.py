
import sqlalchemy
from dash import Dash, html, dcc, Input, Output, callback, State, MATCH, Patch
import pandas as pd
import plotly.graph_objects as go
from configparser import ConfigParser
import time

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


brandin = pd.read_sql_query(
    """SELECT
            CONCAT(GAME_DATE, ' ', MATCHUP) AS MATCHUP_DATE, FAN_PTS, MIN
            FROM players.`Brandin Podziemski`;""",
            engine
)

brandin = brandin.iloc[::-1]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,
           external_stylesheets=external_stylesheets
)

# Take selected player name
df1 = brandin #pd.read_sql_table("Brandin Podziemski", engine)
df2 = pd.read_sql_table("LeBron James", engine)


# show all matchup history
fig1 = go.FigureWidget(
    data=[
        go.Bar(name='BRANDIN PODZIEMSKI', x=df1['MATCHUP_DATE'], y=df1['FAN_PTS'],
               marker_color='#4D935D')],
    layout=go.Layout(
            width = 800,
            margin = dict(l=300, r=200),
            #plot_bgcolor='#101010'
        )
)
# add minutes scatter
fig1.add_trace(
    go.Scatter(mode='lines+markers', name='Minutes played', x=df1['MATCHUP_DATE'], y=df1['MIN'],
               line=dict(color='pink'), marker=dict(color='red'))
)

# add numbers of fan points per game
"""for i, fan_pts in enumerate(df1['FAN_PTS']):
    fig1.add_annotation(
        x=df1['MATCHUP_DATE'][i],
        y=fan_pts + 2,
        text=str(fan_pts),
        showarrow=False,
        font=dict(
            size=8,
            color="Black"
        ),
    )"""

# Specific team matchup history
fig2 = go.FigureWidget(
    data=[
        go.Bar(name='BRANDIN PODZIEMSKI', x=df1['MATCHUP_DATE'], y=df1['MIN'])],
    layout=go.Layout(
            width = 800,
            margin = dict(l=300, r=200)
    )
)

fig2.add_trace(
    go.Scatter(name='Minutes played', x=df1['MATCHUP_DATE'], y=df1['MIN'])
)


# main layout
app.layout = html.Div(
    
    children=[

    # button to update players logs
    html.Button("Update players logs", id="btn_updateLogs"),
    dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1")
        ),

    # search for players
    dcc.Store(id='players-store', storage_type='session'),
    dcc.Dropdown(
        id='player-search-dropdown',
        # here put list of players from mysql
        options=[{'label': player, 'value': player} for player in 
                 ['Lebron James', 'Victor Wembanyama', 'Brandin Podziemski', 'Anthony Davis', 'Stephen Curry']],
        placeholder="Search for a player",
    ),
    html.Div(id='player-search-output', children=[]),

    # tabs to go see through different players added to team
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Player 1', value='tab-1'),
        dcc.Tab(label='Player 2', value='tab-2'),
        dcc.Tab(label='Player 3', value='tab-3'),
        dcc.Tab(label='Player 4', value='tab-4'),
        dcc.Tab(label='Player 5', value='tab-5'),
    ]),
    html.Div(id='tabs-content'),

    # slider to choose number of seen matchups from all history
    dcc.Slider(-5, 10, 1, value=-3),

    # graph showing previous matchup   
    dcc.Graph(
        id='Brandin Podziemski',
        figure=fig1
    ),

    # graph showing previous matchup against chosen opponent
    dcc.Graph(
        id='Victor',
        figure=fig2
    )
])

# loading mark for updating players
@callback(Output("loading-output-1", "children"), Input("btn_updateLogs", "n_clicks"))
def input_triggers_spinner(n_clicks):
    # button not clicked
    if n_clicks is None:
        return None
    # button clicked
    else:
        # here will be function to update players log
        time.sleep(1)
        return "Updating complete"


# searching players
@app.callback(
    Output('player-search-output', 'children'),
    Output('players-store', 'data'),
    Output('player-search-dropdown', 'value'),
    Input('player-search-dropdown', 'value'),
    State('players-store', 'data')
)
def display_selected_player(player, players_list):
    if players_list is None:
        players_list = []
    if player is not None:
        players_list.append(player)
    return dcc.Checklist(options=[{'label': p, 'value': p} for p in players_list]), players_list, None

# displaying tabs of players
@callback(Output('tabs-content', 'children'),
                Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Player 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Player 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Player 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Player 4')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Player 5')
        ])

if __name__ == '__main__':
    app.run(debug=True)
