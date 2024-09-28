# So-Fan Data

SoFan Data is a tool to analyze NBA players for popular Fantasy Sports game Sorare.

### Disclaimer

Project is currently in alpha stage.

What I currently work on?
> Setting next opponent by default.
>
> Displaying average points of a player from the last 10 matches.
>
> Ability to set card bonus percentage.


Branch on which latest changes are available:
> previous_games

## Features

* **NBA API Connection**: Fetches player statistics from the NBA API.
* **Squad Management**: Easy addition and removal of players from user squads.
* **Statistics Analysis**: Implements [Sorare scoring system](https://nbaguide.sorare.com/how-to-play/the-basics/scoring-system) points calculation using Plotly for data visualization.
* **Dash Frontend**: Develops an interactive frontend with Dash for effortless squad building.
* **Team Selection**: Allows users to built teams for weekly Soarer matchups.


## Installation

Make sure you have Python installed.

Then run:
```python
pip install -r requirements.txt
```

To run the app use:
```python
python main.py
```

App will be run on address:
```python
http://127.0.0.1:8050/
```
## License

[MIT](https://choosealicense.com/licenses/mit/)