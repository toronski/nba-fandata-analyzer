from dash import html, dcc
from dropdowns import seasons, games_count, default_games_count, teams_option
from current_season import get_current_season

def display_player_tab(index):

    return html.Div([
                html.Div([
                    dcc.Dropdown(
                        id={'type': 'squad-search-dropdown', 'index': index},
                        options=[],
                        placeholder="Show player info",
                        clearable=False
                    )
                ],
                style={'width': '33%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        seasons, get_current_season(),
                        id={'type': 'season-dropdown', 'index': index},
                        placeholder="Season",
                        clearable=False
                    )
                ],
                style={'width': '16%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        games_count, default_games_count,
                        id={'type': 'num-games-dropdown', 'index': index},
                        placeholder='Games to show'
                    )
                ],
                style={'width': '21%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Dropdown(
                        id={'type': 'opponents-dropdown', 'index': index},
                        options=teams_option,
                        clearable=False 
                        # domyslnie ustawiony nastepny przeciwnik
                    )
                ],
                style={'width': '30%', 'display': 'inline-block'}),

                html.Div(id={'type': 'show-graph1', 'index': index}, children=[]),
                html.Div(id={'type': 'show-graph2', 'index': index}, children=[])
            ])
    