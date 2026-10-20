import os

import pandas as pd
import plotly.graph_objs as go
from dash import Dash, Input, Output, html

os.chdir(os.path.dirname(__file__))

def register_callbacks(app: Dash, df: pd.DataFrame):

    @app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
    )
    def render_content(tab):
        if tab == 'tab-home':
            return html.Div([
                html.H3("Overview"),
                html.P(f"Rows in dataset: {len(df):,}")
            ])

        if tab == 'tab-presentation':
            return html.Div([
                html.H3("Presentation")
            ])

        if tab == 'tab-data':
            return html.Div([
                html.H3("Data Table")
            ])
        if tab == 'tab-graphs':
            return html.Div([
                html.H3("Graphs")
            ])
        if tab == 'tab-animated':
            return html.Div([
                html.H3("Animated")
            ])
        if tab == 'tab-resources':
            return html.Div([
                html.H3("Resources")
            ])