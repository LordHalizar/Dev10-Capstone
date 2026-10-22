import pandas as pd
import plotly.express as px

from dash import dcc, html


def create_game_sales_graph(sales_locations_mapping: dict[str, str]) -> dcc.Graph:

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-regions-dropdown',
                options=[
                    {'label': location, 'value': location} for location in sales_locations_mapping.values()
                ],
                value=list(sales_locations_mapping.values()),
                multi=True,
                placeholder='Select sales regions'
            ),
            dcc.Graph(id='game-sales-graph'),
        ]
    )

def create_genres_region_graph(genres: list[str]) -> dcc.Graph:

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-genres-dropdown',
                options=[
                    {'label': genre, 'value': genre} for genre in genres
                ],
                value=genres,
                multi=True,
                placeholder='Select genres'
            ),
            dcc.Dropdown(
                id='selected-region-dropdown',
                options=[
                    {'label': 'North America', 'value': 'North America'},
                    {'label': 'Japan', 'value': 'Japan'},
                ],
                multi=False,
                value='North America',
                clearable=False
            ),
            dcc.Graph(id='genres-region-graph'),
        ]
    )