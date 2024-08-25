from dash import Dash, html, dcc, Input, Output, State, ctx, MATCH
from nba_api.stats.static import players
from show_previous_games import display_graph
import logging

logging.basicConfig(level=logging.INFO)

external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css']

app = Dash(__name__, suppress_callback_exceptions=True, 
           prevent_initial_callbacks="initial_duplicate",
           external_stylesheets=external_stylesheets,
           meta_tags=[{'name':'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}]
)

app.layout = html.Div(
    className='container',
    children=[
        html.H1("So-Fan STATS", className='item app-header'),

        html.Div(
            className="item search-players",
            children=[
                dcc.Store(id='players-store', storage_type='session'),
                dcc.Dropdown(
                    id='player-search-dropdown',
                    options=[{'label': name['full_name'], 'value': name['full_name']} 
                             for name in players.get_active_players()],
                    placeholder="Search for a player",
                ),
                dcc.Checklist(id='player-search-output', options=[], value=[]),
                html.Button('Remove', id='remove-button', n_clicks=0)
            ]
        ),

        html.Div(
            className="item players-tabs",
            children=[
                dcc.Tabs(id="tabs", value='tab-1',
                        children=[
                            dcc.Tab(label='Player 1', value='tab-1',
                                    children=html.Div([
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-1'},
                                            options=[],
                                            placeholder="Show player info",
                                        ),
                                        html.Div([
                                            dcc.Dropdown(
                                                id='num-games-dropdown',
                                                options=[
                                                    {'label': '5 games', 'value': 5},
                                                    {'label': '10 games', 'value': 10},
                                                    {'label': '15 games', 'value': 15},
                                                    {'label': '25 games', 'value': 25},
                                                ],
                                                placeholder='Games to show'
                                            )
                                        ], 
                                        style={'width': '20%', 'display': 'inline-block'}),
                                        html.Div(id={'type': 'show-graph', 'index': 'tab-1'}, children=[]),
                                    ])
                            ),
                            dcc.Tab(label='Player 2', value='tab-2',
                                    children=html.Div([
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-2'},
                                            options=[],
                                            placeholder="Show player info",
                                        ),
                                        html.Div(id={'type': 'show-graph', 'index': 'tab-2'}, children=[]),
                                    ])
                            ),
                            dcc.Tab(label='Player 3', value='tab-3',
                                    children=html.Div([
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-3'},
                                            options=[],
                                            placeholder="Show player info",
                                        ),
                                        html.Div(id={'type': 'show-graph', 'index': 'tab-3'}, children=[]),
                                    ])
                            ),
                            dcc.Tab(label='Player 4', value='tab-4',
                                    children=html.Div([
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-4'},
                                            options=[],
                                            placeholder="Show player info",
                                        ),
                                        html.Div(id={'type': 'show-graph', 'index': 'tab-4'}, children=[]),
                                    ])
                            ),
                            dcc.Tab(label='Player 5', value='tab-5',
                                    children=html.Div([
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-5'},
                                            options=[],
                                            placeholder="Show player info",
                                        ),
                                        html.Div(id={'type': 'show-graph', 'index': 'tab-5'}, children=[]),
                                    ])
                            ),
                        ]
                )
            ]
        ),
    ]
)

@app.callback(
    Output('player-search-output', 'options'),
    Output('player-search-output', 'value'),
    Output('players-store', 'data'),
    Output('player-search-dropdown', 'value'),
    Input('player-search-dropdown', 'value'),
    Input('remove-button', 'n_clicks'),
    State('player-search-output', 'value'),
    State('players-store', 'data')
)
def update_players(player, n_clicks, selected_players, players_list):
    trigger = ctx.triggered_id

    if players_list is None:
        players_list = []

    if trigger == 'player-search-dropdown' and player:
        if player not in players_list:
            players_list.append(player)
        new_value = []
    elif trigger == 'remove-button' and selected_players:
        players_list = [p for p in players_list if p not in selected_players]
        new_value = []
    else:
        new_value = selected_players

    options = [{'label': p, 'value': p} for p in players_list]
    
    return options, new_value, players_list, None

@app.callback(
    Output({'type': 'squad-search-dropdown', 'index': MATCH}, 'options'),
    Input('players-store', 'data')
)
def update_tab_dropdown_options(stored_data):
    if stored_data is None:
        return []
    return [{'label': player, 'value': player} for player in stored_data]

@app.callback(
    Output({'type': 'show-graph', 'index': MATCH}, 'children'),
    Input({'type': 'squad-search-dropdown', 'index': MATCH}, 'value'),
    Input('num-games-dropdown', 'value')
)
def show_previous_games(player_name, games_number):
    if player_name is None:
        return None
    # dodac argument z liczba gier
    # dodac osobny dropdown menu do glownego layoutu
    return display_graph(player_name, games_number)

if __name__ == '__main__':
    app.run(debug=True)
