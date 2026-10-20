import os

import pandas as pd
from callbacks import register_callbacks
from dash import Dash, dcc, html
from dynaconf import Dynaconf
from sqlalchemy import Engine, create_engine

os.chdir(os.path.dirname(__file__))

def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
    return create_engine(settings.ENGINE_URL, echo=True)

engine = build_engine()

query = """
    select
        ga.game_title,
        pl.platform_name,
        ge.genre_name,
        min(ga.release_year) as earliest_release_year,
        sum(s.na_sales) as na_sales,
        sum(s.jp_sales) as jp_sales
    from game_platform gp
    join game ga on ga.game_id = gp.game_id
    join genre ge on ge.genre_id = ga.genre_id
    join platform pl on pl.platform_id = gp.platform_id
    join sales s on s.game_platform_id = gp.game_platform_id
    group by 
        ga.game_title, 
        pl.platform_name, 
        ge.genre_name
    order by 
        min(ga.release_year), 
        ga.game_title, 
        pl.platform_name;
"""

df = pd.read_sql(query, engine)

app = Dash(__name__, suppress_callback_exceptions=False)

app.layout = html.Div([
    dcc.Loading(
        html.Div([
            dcc.Tabs(
                id='tabs',
                value='tab-home',
                children=[
                    dcc.Tab(label='Home', value='tab-home'),
                    dcc.Tab(label='Presentation', value='tab-presentation'),
                    dcc.Tab(label='Data Table', value='tab-data'),
                    dcc.Tab(label='Graphs', value='tab-graphs'),
                    dcc.Tab(label='Animated Graphs', value='tab-animated'),
                    dcc.Tab(label='Resources & Citations', value='tab-resources'),
                ]
            ),
            html.Div(id='tabs-content')
        ])
    )
])

# register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True, dev_tools_props_check=False)