
from dash import Dash, html, dcc, Input, Output, callback, State, MATCH, Patch
from players_data import save_games_log, get_players_ids, save_active_players
import mysql_connector
from player_class import Player


engine = mysql_connector.engine

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css']

app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           # response to mobile
           meta_tags=[{'name':'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}]
)


# add dropdown menu to graph
"""
fig1.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["type", "surface"],
                    label="3D Surface",
                    method="restyle"
                ),
                dict(
                    args=["type", "heatmap"],
                    label="Heatmap",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)
"""
# add numbers of fan points per game
"""
for i, fan_pts in enumerate(df1['FAN_PTS']):
    fig1.add_annotation(
        x=df1['MATCHUP_DATE'][i],
        y=fan_pts + 2,
        text=str(fan_pts),
        showarrow=False,
        font=dict(
            size=8,
            color="Black"
        ),
    )
"""


# main layout
app.layout = html.Div(
    className='container',
    children=[
        html.H1("So-Fan STATS",
                className='item app-header'
        ),

        # search for players
        html.Div(
            className="item search-players",
            children=[
                dcc.Store(id='players-store', storage_type='session'),
                dcc.Dropdown(
                    id='player-search-dropdown',
                    # here put list of players from mysql
                    options=[{'label': player, 'value': player} for player in
                            [name['full_name'] for name in get_players_ids()]
                    ],
                    placeholder="Search for a player",
                ),
                html.Div(id='player-search-output', children=[]),
                html.Button('Remove', id='remove-button', n_clicks=0)
            ]
        ),
        # Tabs to go see through different players added to team
        html.Div(
            className="item players-tabs",
            children = [
                dcc.Tabs(id="tabs", value='tab-1',
                        children=[
                            dcc.Tab(label='Player 1', value='tab-1'),
                            dcc.Tab(label='Player 2', value='tab-2'),
                            dcc.Tab(label='Player 3', value='tab-3'),
                            dcc.Tab(label='Player 4', value='tab-4'),
                            dcc.Tab(label='Player 5', value='tab-5'),
                        ]
                ),
                html.Div(
                    id='tabs-content',
                )    
            ]
        ),


        html.Div(
            className='item refresh-players',
            children=[
                # button to update players logs
                html.Button("Update players logs", id="btn_updateLogs"),
                dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div(id="loading-output-1")
                )
            ]
        )
    ]
)

# loading mark for updating players
@app.callback(Output("loading-output-1", "children"), Input("btn_updateLogs", "n_clicks"))
def input_triggers_spinner(n_clicks):
    # button not clicked
    if n_clicks is None:
        return None
    # button clicked
    else:
        # function to update players log
        save_active_players()
        id, name = get_players_ids()
        save_games_log(id, name)
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
        # iterate through players list with dict of specific player
        data = get_players_ids() # for each dict
        for index in data:
            if index['full_name'] == player:
                player = Player(index['id'], player) # create player class
                # add player name to your squad
                players_list.append(str(player))
    options = [{'label': p, 'value': p} for p in players_list]
    return dcc.Checklist(options=options), players_list, None

# displaying tabs of players
@app.callback(Output('tabs-content', 'children'),
                Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Player 1'),
                # graph showing previous matchup   
                
                # graph showing previous matchup against chosen opponent
        ]),

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
