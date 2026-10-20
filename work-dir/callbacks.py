import os

import pandas as pd
import plotly.graph_objs as go
from dash import Dash, Input, Output, dcc, html

os.chdir(os.path.dirname(__file__))

def register_callbacks(app: Dash, df: pd.DataFrame):

    @app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
    )
    def render_content(tab):
        pass