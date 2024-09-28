from nba_api.stats.library.parameters import SeasonAll

seasons = [
    SeasonAll.all,
    '2023-24',
    '2022-23'
    ]

default_games_count = 10

games_count = [
    {'label': '5 games', 'value': 5},
    {'label': '10 games', 'value': 10},
    {'label': '15 games', 'value': 15},
    {'label': '25 games', 'value': 25},
    {'label': '50 games', 'value': 50}
]

teams_option = [
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
]