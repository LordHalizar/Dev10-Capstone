import os

import pandas as pd
from callbacks import register_callbacks
from dynaconf import Dynaconf
from sqlalchemy import Engine, create_engine

from dash import Dash, dcc, html

os.chdir(os.path.dirname(__file__))

def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
    return create_engine(settings.ENGINE_URL, echo=True)

engine = build_engine()

query = """
    with game_genres as (
        select 
            gg.game_id,
            string_agg(distinct g.genre_name, ', ' order by g.genre_name) as genres
        from game_genre gg
        join genre g on g.genre_id = gg.genre_id
        group by gg.game_id
    ),
    game_publishers as (
        select
            gp.game_id,
            string_agg(distinct p.publisher_name, ', ' order by p.publisher_name) as publishers
        from game_publisher gp
        join publisher p on p.publisher_id = gp.publisher_id
        group by gp.game_id  
    )
    select 
        ga.game_title,
        r.release_year,
        gg.genres,
        gp.publishers,
        pl.platform_name,
        s.na_sales,
        s.jp_sales
    from game_platform_release r
    join game_platform gpl on gpl.game_platform_id = r.game_platform_id
    join game ga on ga.game_id = gpl.game_id
    join game_genres gg on gg.game_id = ga.game_id
    join game_publishers gp on gp.game_id = ga.game_id
    join platform pl on pl.platform_id = gpl.platform_id
    join sales s on s.game_platform_release_id = r.game_platform_release_id
    order by r.release_year, ga.game_title, pl.platform_name;
"""

df = pd.read_sql(query, engine)

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Loading(
        children=html.Div([
            dcc.Tabs(
                id='tabs',
                value='tab-home',
                className='app-tabs',
                children=[
                    dcc.Tab(label='⌂ Home', value='tab-home', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='♙ Slides', value='tab-presentation', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='◇ Data Table', value='tab-data', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='▥ Sales', value='tab-sales-graphs', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='▥ Genre', value='tab-genre-graphs', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='▥ Platform', value='tab-platform-graphs', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='▥ Publisher', value='tab-publisher-graphs', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='▥ Graphs', value='tab-graph-pics', className='app-tab', selected_className='app-tab--selected'),
                    # dcc.Tab(label='◉ Animated Graphs', value='tab-animated', className='app-tab', selected_className='app-tab--selected'),
                    dcc.Tab(label='⚒ Resources', value='tab-resources', className='app-tab', selected_className='app-tab--selected'),
                ]
            ),
            html.Div(id='tabs-content', className='content-panel')
        ])
    )
])

register_callbacks(app, df)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True, dev_tools_props_check=False)