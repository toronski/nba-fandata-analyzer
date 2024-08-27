from dash import Dash, html, dcc, Input, Output, State, ctx, MATCH
from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerNextNGames
from show_previous_games import previous_games_graph, one_previous_opponent
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
                            dcc.Tab(id={'type': 'dynamic-tab', 'index': 'tab-1'}, value='tab-1', className='custom-tab-label',
                                    children=html.Div([
                                        html.Div([
                                            dcc.Dropdown(
                                                id={'type': 'squad-search-dropdown', 'index': 'tab-1'},
                                                options=[],
                                                placeholder="Show player info",
                                                clearable=False
                                            )],
                                        style={'width': '33%', 'display': 'inline-block'}),
                                        html.Div([
                                            dcc.Dropdown(
                                                ['2023-24', '2022-23'], '2023-24', # ustawic podglad na kilka sezonow
                                                id='season-dropdown',
                                                placeholder="Season",
                                                clearable=False
                                            )],
                                        style={'width': '16%', 'display': 'inline-block'}),
                                        html.Div([
                                            dcc.Dropdown(
                                                [
                                                    {'label': '5 games', 'value': 5},
                                                    {'label': '10 games', 'value': 10},
                                                    {'label': '15 games', 'value': 15},
                                                    {'label': '25 games', 'value': 25},
                                                ], 5,
                                                id='num-games-dropdown',
                                                placeholder='Games to show'
                                            )
                                        ], 
                                        style={'width': '21%', 'display': 'inline-block'}),
                                        html.Div([
                                            dcc.Dropdown(
                                                id='opponents-dropdown',
                                                options=[
                                                    {'label': 'Atlanta Hawks', 'value': 'ATL'},
                                                    {'label': 'Boston Celtics', 'value': 'BOS'},
                                                    {'label': 'Brooklyn Nets', 'value': 'BKN'},
                                                    {'label': 'Charlotte Hornets', 'value': 'CHA'},
                                                    {'label': 'Chicago Bulls', 'value': 'CHI'},
                                                    {'label': 'Cleveland Cavaliers', 'value': 'CLE'},
                                                    {'label': 'Dallas Mavericks', 'value': 'DAL'},
                                                    {'label': 'Denver Nuggets', 'value': 'DEN'},
                                                    {'label': 'Detroit Pistons', 'value': 'DET'},
                                                    {'label': 'Golden State Warriors', 'value': 'GSW'},
                                                    {'label': 'Houston Rockets', 'value': 'HOU'},
                                                    {'label': 'Indiana Pacers', 'value': 'IND'},
                                                    {'label': 'Los Angeles Clippers', 'value': 'LAC'},
                                                    {'label': 'Los Angeles Lakers', 'value': 'LAL'},
                                                    {'label': 'Memphis Grizzlies', 'value': 'MEM'},
                                                    {'label': 'Miami Heat', 'value': 'MIA'},
                                                    {'label': 'Milwaukee Bucks', 'value': 'MIL'},
                                                    {'label': 'Minnesota Timberwolves', 'value': 'MIN'},
                                                    {'label': 'New Orleans Pelicans', 'value': 'NOP'},
                                                    {'label': 'New York Knicks', 'value': 'NYK'},
                                                    {'label': 'Oklahoma City Thunder', 'value': 'OKC'},
                                                    {'label': 'Orlando Magic', 'value': 'ORL'},
                                                    {'label': 'Philadelphia 76ers', 'value': 'PHI'},
                                                    {'label': 'Phoenix Suns', 'value': 'PHX'},
                                                    {'label': 'Portland Trail Blazers', 'value': 'POR'},
                                                    {'label': 'Sacramento Kings', 'value': 'SAC'},
                                                    {'label': 'San Antonio Spurs', 'value': 'SAS'},
                                                    {'label': 'Toronto Raptors', 'value': 'TOR'},
                                                    {'label': 'Utah Jazz', 'value': 'UTA'},
                                                    {'label': 'Washington Wizards', 'value': 'WAS'}
                                                ], clearable=False
                                            )
                                        ],
                                        style={'width': '30%', 'display': 'inline-block'}),
                        
                                        html.Div(id={'type': 'show-graph1', 'index': 'tab-1'}, children=[]),
                                        html.Div(id={'type': 'show-graph2', 'index': 'tab-1'}, children=[])
                                        # domyslnie ustawiony nastepny przeciwnik
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
    Output({'type': 'dynamic-tab', 'index': MATCH}, 'label'),
    Input({'type': 'squad-search-dropdown', 'index': MATCH}, 'value')
)
def update_tab_label(player_name):
    if player_name is None:
        return 'Empty'
    return player_name

@app.callback(
    Output({'type': 'show-graph1', 'index': MATCH}, 'children'),
    Input({'type': 'squad-search-dropdown', 'index': MATCH}, 'value'),
    Input('num-games-dropdown', 'value'),
    Input('season-dropdown', 'value')
)
def previous_games(player_name, games_number, season):
    if player_name is None:
        return None
    return previous_games_graph(player_name, games_number, season)

@app.callback(
    Output({'type': 'show-graph2', 'index': MATCH}, 'children'),
    Input({'type': 'squad-search-dropdown', 'index': MATCH}, 'value'),
    Input('season-dropdown', 'value'),
    Input('opponents-dropdown', 'value')
)
def previous_opponent(player_name, season, team_filter, games_number=100):
    if player_name is None:
        return None
    return one_previous_opponent(player_name, games_number, season, team_filter)
    

if __name__ == '__main__':
    app.run(debug=True)
