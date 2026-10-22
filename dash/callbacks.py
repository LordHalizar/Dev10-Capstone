import os

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from dash import Dash, Input, Output, State, dash_table, dcc, html

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

        if tab == "tab-data":

            return html.Div(
                className="tab-panel",
                children=[
                    html.H3("Data Table", className='tab-panel-title'),
                    dash_table.DataTable(
                        id="dataset-table",
                        columns=[
                            {"name": str(column), "id": str(column)}
                            for column in df.columns
                        ],
                        data=df.to_dict("records"),
                        page_size=20,
                        sort_action="native",
                        filter_action="native",
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "left",
                            "padding": "10px 12px",
                            "maxWidth": "250px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                        },
                        style_header={
                            "backgroundColor": "#24bd88",
                            "color": "white",
                            "fontWeight": "600",
                        },
                    ),
                ],
            )
        if tab == 'tab-graphs':
            sales_locations_mapping = {
                'na_sales': 'North America',
                'jp_sales': 'Japan'
            }
            
            all_genres = sorted({
                genre.strip()
                for genres in df['genres'].dropna()
                for genre in (
                    genres.split(', ') if isinstance(genres, str) else genres
                )
                if isinstance(genre, str) and genre.strip()
            })

            return html.Div(
                className='tab-panel',
                children=[
                    html.H3("Graphs", className='tab-panel-title'),
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
                    dcc.Dropdown(
                        id='selected-genres-dropdown',
                        options=[
                            {'label': genre, 'value': genre} for genre in all_genres
                        ],
                        value=all_genres,
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
        if tab == 'tab-animated':
            return html.Div([
                html.H3("Animated")
            ])
        if tab == 'tab-resources':
            return html.Div([
                html.H3("Resources")
            ])
        
    @app.callback(
        Output('genres-region-graph', 'figure'),
        Input('selected-regions-dropdown', 'value')
    )
    def update_sales_graph(selected_regions):

        date_column = 'release_year'
        sales_columns_mapping = {
            'na_sales': 'North America',
            'jp_sales': 'Japan'
        }
        label_mapping = {
            'release_year': 'Release Year',
            'sales': 'Units Sold (millions)',
            'region': 'Region'
        }
        title = "Video Game Sales by Release Year"
        
        if not selected_regions:
            return px.line(
                title='Select at least one region to display sales'
            )

        sales_long = df.melt(
            id_vars=date_column,
            value_vars=sales_columns_mapping.keys(),
            var_name='region',
            value_name='sales'
        )

        sales_long[date_column] = pd.to_numeric(
            sales_long[date_column], errors='coerce'
        )

        sales_long['sales'] = pd.to_numeric(sales_long['sales'], errors='coerce')
        sales_long = sales_long.dropna(subset=[date_column, 'sales'])

        sales_long['region'] = sales_long['region'].map(
            sales_columns_mapping
        )

        annual_sales = (
            sales_long.groupby([date_column, 'region'], as_index=False)['sales']
            .sum()
            .sort_values(date_column)
        )
        
        filtered = annual_sales[
            annual_sales['region'].isin(selected_regions)
        ]

        fig = px.line(
            filtered,
            x=date_column,
            y='sales',
            color='region',
            markers=False,
            labels=label_mapping,
            title=title
        )

        return fig

    df['genres'] = df['genres'].fillna('').str.split(', ')

    genre_rows = df.explode('genres').rename(columns={'genres': 'genre'})
    genre_rows = genre_rows[genre_rows['genre'] != '']

    sales_by_year_genre = (
        genre_rows
        .groupby(['release_year', 'genre'], as_index=False)
        .agg(
            na_sales=('na_sales', 'sum'),
            jp_sales=('jp_sales', 'sum')
        )
    )

    @app.callback(
        Output('genres-region-graph', 'figure'),
        Input('selected-genres-dropdown', 'value'),
        Input('selected-region-dropdown', 'value')
    )
    def update_region_genres_graph(selected_genres, selected_region):
        
        if not selected_genres:
            return px.line(
                title='Select at least one genre to display sales'
            )

        selected_genres = selected_genres or []

        regions_columns = {
            'North America': ('na_sales', 'North America Sales'),
            'Japan': ('jp_sales', 'Japan Sales')
        }

        if not selected_region or selected_region not in regions_columns:
            return px.line(
                title='Select a valid sales region'
            )

        sales_column, sales_label = regions_columns[selected_region]

        filtered = sales_by_year_genre[
            sales_by_year_genre['genre'].isin(selected_genres)
        ]

        fig = px.line(
            filtered,
            x='release_year',
            y=sales_column,
            color='genre',
            markers=False,
            labels={
                'release_year': 'Release Year',
                sales_column: sales_label,
                'genre': 'Genre'
            },
            title=f"{sales_label} Game Sales by Genre and Year"
        )

        return fig

    @app.callback(
        Output('genre-sales-graph', 'figure'),
        Input('selected-genre-dropdown', 'value'),
        Input('selected-region-dropdown', 'value')
    )
    def update_regions_genre_graph(selected_genres, selected_region):
        
        if not selected_genres:
            return px.line(
                title='Select at least one genre to display sales'
            )

        selected_genres = selected_genres or []

        regions_columns = {
            'North America': ('na_sales', 'North America Sales'),
            'Japan': ('jp_sales', 'Japan Sales')
        }

        if not selected_region or selected_region not in regions_columns:
            return px.line(
                title='Select a valid sales region'
            )

        sales_column, sales_label = regions_columns[selected_region]

        filtered = sales_by_year_genre[
            sales_by_year_genre['genre'].isin(selected_genres)
        ]

        fig = px.line(
            filtered,
            x='release_year',
            y=sales_column,
            color='genre',
            markers=False,
            labels={
                'release_year': 'Release Year',
                sales_column: sales_label,
                'genre': 'Genre'
            },
            title=f"{sales_label} Game Sales by Genre and Year"
        )

        return fig