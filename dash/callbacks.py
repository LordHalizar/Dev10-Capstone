import os

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from tab_graphs import (
    create_game_sales_graph,
    create_genres_region_graph,
    create_platforms_region_graph,
    create_publishers_region_graph,
    create_regions_genre_graph,
)

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
                className="tab-graph",
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

        if tab == 'tab-genre-graphs':
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
                    create_genres_region_graph(all_genres),
                    create_regions_genre_graph(genres=all_genres, regions=['North America', 'Japan']),
                ]
            )

        if tab == 'tab-platform-graphs':
            all_platforms = sorted(
                platform.strip()
                for platform in df['platform_name'].dropna().unique()
                if isinstance(platform, str) and platform.strip()
            )
        
            return html.Div(
                className='tab-panel',
                children=[
                    create_platforms_region_graph(platforms=all_platforms, regions_mapping=REGIONS_MAPPING)
                ]
            )

        
        if tab == 'tab-publisher-graphs':
            sales_locations_mapping = {
                'na_sales': 'North America',
                'jp_sales': 'Japan'
            }

            all_publishers = sorted({
                publisher.strip()
                for publishers in df['publishers'].dropna()
                for publisher in (
                    publishers.split(', ') if isinstance(publishers, str) else publishers
                )
                if isinstance(publisher, str) and publisher.strip()
            })

            return html.Div(
                className='tab-panel',
                children=[
                    create_game_sales_graph(sales_locations_mapping), 
                    create_publishers_region_graph(publishers=all_publishers, regions_mapping=REGIONS_MAPPING),
                ]
            )

        if tab == 'tab-graph-pics':
            return html.Div([
                html.H3("Graph Pics")
            ])

        if tab == 'tab-animated':
            return html.Div([
                html.H3("Animated")
            ])
        if tab == 'tab-resources':
            return html.Div([
                html.H3("Resources")
            ])

    REGION_COLUMNS = {
        'North America': 'na_sales',
        'Japan': 'jp_sales'
    }
        
    @app.callback(
        Output('game-sales-graph', 'figure'),
        Input('selected-sales_regions-dropdown', 'value')
    )
    def update_sales_graph(selected_regions):

        selected_regions = selected_regions or []

        region_columns = [
            REGION_COLUMNS[region]
            for region in selected_regions
            if region in REGION_COLUMNS
        ]

        if not region_columns:
            return px.line(title="Select at least one region.")

        yearly_sales = df.groupby('release_year', as_index=False)[
            ['na_sales', 'jp_sales']
        ].sum()

        fig = px.line(
            data_frame=yearly_sales,
            x='release_year',
            y=region_columns,
            labels={
                'release_year': 'Release Year',
                'value': 'Sales',
                'variable': 'Region'
            },
            title='Video Game Sales by Release Year'
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

    REGIONS_MAPPING = {
        'North America': ('na_sales', 'North America Sales'),
        'Japan': ('jp_sales', 'Japan Sales')
    }


    @app.callback(
        Output('genres-region-graph', 'figure'),
        Input('selected-genres-dropdown', 'value'),
        Input('selected-region-dropdown', 'value')
    )
    def update_genres_region_graph(selected_genres, selected_region):
        
        if not selected_genres:
            return px.line(title="Select at least one genre.")

        sales_column, sales_label = REGIONS_MAPPING.get(selected_region, (None, None))

        if sales_column is None:
            return px.line(title="Select a valid sales region.")

        data = sales_by_year_genre[
            sales_by_year_genre['genre'].isin(selected_genres)
        ]

        fig = px.line(
            data_frame=data,
            x='release_year',
            y=sales_column,
            color='genre',
            labels={
                'release_year': 'Release Year',
                sales_column: sales_label,
                'genre': 'Genre'
            },
            title=f"{sales_label} Game Sales by Genre and Year"
        )

        return fig

    @app.callback(
        Output('regions-genre-graph', 'figure'),
        Input('selected-genre-dropdown', 'value'),
        Input('selected-regions-dropdown', 'value')
    )
    def update_regions_genre_graph(selected_genre, selected_regions):
        
        if not selected_genre:
            return px.line(title="Select at a genre.")

        if not selected_regions:
            return px.line(title="Select at least one sales region.")

        data = sales_by_year_genre[
            sales_by_year_genre['genre'] == selected_genre
        ]

        colors = px.colors.qualitative.Plotly

        first_column, first_label = REGIONS_MAPPING[selected_regions[0]]

        fig = px.line(
            data_frame=data,
            x='release_year',
            y=first_column,
            title=f"{selected_genre} Sales by Region and Year",
            labels={
                'release_year': 'Release Year',
                first_column: 'Sales (millions)'
            }
        )
        fig.update_traces(name=first_label, showlegend=True, line=dict(color=colors[0]))

        for i, region in enumerate(selected_regions[1:], start=1):
            sales_column, sales_label = REGIONS_MAPPING[region]

            extra_line = px.line(
                data_frame=data,
                x='release_year',
                y=sales_column
            )
            extra_line.update_traces(name=sales_label, showlegend=True, line=dict(color=colors[i % len(colors)]))
            fig.add_traces(extra_line.data)

        fig.update_layout(
            xaxis_title='Release Year',
            yaxis_title='Sales (millions)',
            legend_title_text='Region'
        )

        return fig

    publisher_rows = df.explode('publishers').rename(columns={'publishers': 'publisher'})
    publisher_rows = publisher_rows[publisher_rows['publisher'] != '']

    sales_by_year_publisher = (
        publisher_rows
        .groupby(['release_year', 'publisher'], as_index=False)
        .agg(
            na_sales=('na_sales', 'sum'),
            jp_sales=('jp_sales', 'sum')
        )
    )

    @app.callback(
        Output('publishers-region-graph', 'figure'),
        Input('selected-R_publishers-dropdown', 'value'),
        Input('selected-P_region-dropdown', 'value')
    )
    def update_publishers_region_graph(selected_publishers, selected_region):
        
        if not selected_publishers:
            return px.line(title="Select at least one publisher.")

        sales_column, sales_label = REGIONS_MAPPING.get(selected_region, (None, None))

        if sales_column is None:
            return px.line(title="Select a valid sales region.")

        data = sales_by_year_publisher[
            sales_by_year_publisher['publisher'].isin(selected_publishers)
        ]

        fig = px.line(
            data_frame=data,
            x='release_year',
            y=sales_column,
            color='publisher',
            labels={
                'release_year': 'Release Year',
                sales_column: sales_label,
                'publisher': 'Publisher'
            },
            title=f"{sales_label} Game Sales by Publisher and Year"
        )

        return fig

    platform_rows = df[df['platform_name'] != '']

    sales_by_year_platform = (
        platform_rows
        .groupby(['release_year', 'platform_name'], as_index=False)
        .agg(
            na_sales=('na_sales', 'sum'),
            jp_sales=('jp_sales', 'sum')
        )
    )

    @app.callback(
        Output('platforms-region-graph', 'figure'),
        Input('selected-platforms-dropdown', 'value'),
        Input('selected-Pl_region-dropdown', 'value')
    )
    def update_platform_regions_graph(selected_platforms, selected_region):
        
        if not selected_platforms:
            return px.line(title="Select at least one platform/console.")

        sales_column, sales_label = REGIONS_MAPPING.get(selected_region, (None, None))

        if sales_column is None:
            return px.line(title="Select a valid sales region.")

        data = sales_by_year_platform[
            sales_by_year_platform['platform_name'].isin(selected_platforms)
        ]

        fig = px.line(
            data_frame=data,
            x='release_year',
            y=sales_column,
            color='platform_name',
            labels={
                'release_year': 'Release Year',
                sales_column: sales_label,
                'platform_name': 'Platform'
            },
            title=f"{sales_label} Game Sales by Platform and Year"
        )

        return fig