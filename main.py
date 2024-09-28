from dash import Dash, html, dcc, Input, Output, State, ctx, MATCH
from nba_api.stats.static import players
from show_previous_games import previous_games_graph, one_previous_opponent
import logging
from nba_api.stats.library.parameters import SeasonAll
from player_tab import display_player_tab

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

                            dcc.Tab(id={'type': 'dynamic-tab', 'index': 'tab-1'}, 
                                value='tab-1', 
                                className='custom-tab-label',
                                
                                children=display_player_tab('tab-1')),

                            dcc.Tab(id={'type': 'dynamic-tab', 'index': 'tab-2'}, 
                                value='tab-2', 
                                className='custom-tab-label',
                                
                                children=display_player_tab('tab-2')),

                            dcc.Tab(id={'type': 'dynamic-tab', 'index': 'tab-3'}, 
                                value='tab-3', 
                                className='custom-tab-label',
                                
                                children=display_player_tab('tab-3')),

                            dcc.Tab(id={'type': 'dynamic-tab', 'index': 'tab-4'}, 
                                value='tab-4', 
                                className='custom-tab-label',
                                
                                children=display_player_tab('tab-4')),

                            dcc.Tab(id={'type': 'dynamic-tab', 'index': 'tab-5'}, 
                                value='tab-5', 
                                className='custom-tab-label',
                                
                                children=display_player_tab('tab-5'))
                        ]
                ),
            ]
        )
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
    Input({'type': 'num-games-dropdown', 'index': MATCH}, 'value'),
    Input({'type': 'season-dropdown', 'index': MATCH}, 'value')
)
def previous_games(player_name, games_number, season):
    if player_name is None:
        return None
    return previous_games_graph(player_name, games_number, season)

@app.callback(
    Output({'type': 'show-graph2', 'index': MATCH}, 'children'),
    Input({'type': 'squad-search-dropdown', 'index': MATCH}, 'value'),
    Input({'type': 'opponents-dropdown', 'index': MATCH}, 'value')
)
def previous_opponent(player_name, team_filter, games_number=150):
    if player_name is None:
        return None
    return one_previous_opponent(player_name, games_number, SeasonAll.all, team_filter)
    

if __name__ == '__main__':
    app.run(debug=True)
