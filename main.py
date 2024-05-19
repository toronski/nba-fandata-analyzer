
from dash import Dash, html, dcc, Input, Output, callback, State, MATCH, Patch, no_update
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import plotly.graph_objects as go


external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css']

app = Dash(__name__, suppress_callback_exceptions=True,
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
                    # getting dict with ids and names from mysql, extracting names
                    options=[{'label': name['full_name'], 'value': name['full_name']} 
                            for name in players.get_active_players()
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
                            dcc.Tab(label='Player 1', value='tab-1',
                                    children=html.Div([
                                        # graph showing previous matchup   
                                        dcc.Dropdown(
                                            id='squad-search-dropdown',
                                            options=[], # list of stored players
                                            placeholder="Show player info",
                                        ),
                                        html.Div(id='show-graph-1', children=[]),
                                    ])
                            ),
                            dcc.Tab(label='Player 2', value='tab-2',
                                    children=html.Div([
                                        # graph showing previous matchup   
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-2'},
                                            # here put list of players from mysql
                                            placeholder="Show player info",
                                        ),
                                    ])
                            ),
                            dcc.Tab(label='Player 3', value='tab-3',
                                    children=html.Div([
                                        # graph showing previous matchup   
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-3'},
                                            # here put list of players from mysql
                                            placeholder="Show player info",
                                        ),
                                    ])
                            ),
                            dcc.Tab(label='Player 4', value='tab-4',
                                    children=html.Div([
                                        # graph showing previous matchup   
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-4'},
                                            # here put list of players from mysql
                                            placeholder="Show player info",
                                        ),
                                    ])
                            ),
                            dcc.Tab(label='Player 5', value='tab-5',
                                    children=html.Div([
                                        # graph showing previous matchup   
                                        dcc.Dropdown(
                                            id={'type': 'squad-search-dropdown', 'index': 'tab-5'},
                                            # here put list of players from mysql
                                            placeholder="Show player info",
                                        ),
                                    ])
                            ),
                        ]
                )
            ]
        ),
    ]
)


# searching players
@app.callback(
    Output('player-search-output', 'children'),
    Output('players-store', 'data'),
    Output('player-search-dropdown', 'value'),
    Input('player-search-dropdown', 'value'),
    State('players-store', 'data')
)
def add_selected_player_to_club(player, players_list):
    if players_list is None:
        players_list = []
    if player is not None:
        players_list.append(player)
    
    options = [{'label': p, 'value': p} for p in players_list]
    return dcc.Checklist(options=options), players_list, None

# squad dropdown
@app.callback(
    Output('squad-search-dropdown', 'options'),
    Input('players-store', 'data')
)
def update_dropdown_options(stored_data):
    if stored_data is None:
        return []
    return [{'label': player, 'value': player} for player in stored_data]


@app.callback(
        Output('show-graph-1', 'children'),
        Input('squad-search-dropdown', 'value')
)
def show_previous_games(player_name):
        if player_name is None:
            return None
        # find player ID
        player_id = players.find_players_by_full_name(player_name)[0]['id']
        # download game log of a player
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24').get_data_frames()[0]
        # get player info needed for 
        games = game_log.head(10)
       
        # built all matchup history
        fig = go.FigureWidget(
            data=[
                go.Bar(
                    name=player_name,
                    x=games['GAME_DATE'],
                    y=games['MIN'],
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


'''
# displaying tabs of players
@app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
        Input('squad-search-dropdown', 'value')
)
def render_content(tab, player_name):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Player 1'),
            # graph showing previous matchup   
            dcc.Dropdown(
                id='squad-search-dropdown',
                # here put list of players from mysql
                options=[],
                placeholder="Search for a player",
            ),
            html.Div(id='squad-search-output', children=[]),
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


# searching players
@app.callback(
    Output('player-search-output', 'children'),
    Output('player-search-dropdown', 'value'),
    Input('player-search-dropdown', 'value',),
)
def display_selected_player(player):
    if players_list is None:
        players_list = []
    if player is not None and player != '':
        # iterate through players list with dict of specific player
        # data = get_players_ids() # for each dict
        # for index in data:
        #     if index['full_name'] == player:
        #         player = Player(index['id'], player) # create player class
        #         # add player name to your squad
        #         players_list.append({'id': player.get_id(), 'name': str(player)})
        players_list.append(player)
        options = [{'label': p, 'value': p} for p in players_list]
        return dcc.Checklist(options=options), players_list, None
    return None, players_list, None


@app.callback(
        Output('show-graph', 'children'),
        Input('squad-search-dropdown', 'options')
)
def show_player_graph(player):
    if player is None:
        return None
    else:
        player.show_previous_games()
    
'''
if __name__ == '__main__':
    app.run(debug=True)
