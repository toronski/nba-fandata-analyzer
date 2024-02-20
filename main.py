
import sqlalchemy
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

engine = sqlalchemy.create_engine('mysql+pymysql://root:lakmunsen115@localhost/players')


app = Dash(__name__)

# Take selected player name
df1 = pd.read_sql_table("Brandin Podziemski", engine)
df2 = pd.read_sql_table("Victor Wembanyama", engine)


# All matchup history
fig1 = go.FigureWidget(
    data=[
        go.Bar(name='BRANDIN PODZIEMSKI', x=df1['GAME_DATE'], y=df1['MIN'])],
    layout=go.Layout(
            width = 800,
            margin = dict(l=300, r=200)
        )
)

fig1.add_trace(
    go.Scatter(name='Minutes played', x=df1['GAME_DATE'], y=df1['MIN'])
)

# Specific team matchup history
fig2 = go.FigureWidget(
    data=[
        go.Bar(name='BRANDIN PODZIEMSKI', x=df1['GAME_DATE'], y=df1['MIN'])],
    layout=go.Layout(
            width = 800,
            margin = dict(l=300, r=200)
    )
)

fig2.add_trace(
    go.Scatter(name='Minutes played', x=df1['GAME_DATE'], y=df1['MIN'])
)

app.layout = html.Div(children=[
    dcc.Graph(
        id='Brandin Podziemski',
        figure=fig1
    ),

    dcc.Graph(
        id='Victor Wembanyama',
        figure=fig2
    )
])

if __name__ == '__main__':
    app.run(debug=True)
