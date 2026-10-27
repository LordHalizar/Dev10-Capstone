import os

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from callback_dfs import VideoGameDataFrames
from callback_selection_options import VideoGameSelectionOptions
from tab_graphs import (
    create_animated_sales_by_year_genre,
    create_animated_sales_by_year_platform,
    create_game_sales_graph,
    create_game_sales_scatter,
    create_genres_region_graph,
    create_platforms_region_graph,
    create_publishers_region_graph,
    create_regions_genre_graph,
    update_graph_style2,
)

from dash import Dash, Input, Output, State, dash_table, dcc, html

os.chdir(os.path.dirname(__file__))

REGIONS_MAPPING = {
    'North America': ('na_sales', 'North America Sales'),
    'Japan': ('jp_sales', 'Japan Sales')
}

REGION_COLUMNS = {
    'North America': 'na_sales',
    'Japan': 'jp_sales'
}

slide_paths = [
    "/assets/slides/Capstone_slide_1.png",
    "/assets/slides/Capstone_slide_2.png",
    "/assets/slides/Capstone_slide_3.png",
    "/assets/slides/Capstone_slide_4.png",
    "/assets/slides/Capstone_slide_5.png",
    "/assets/slides/Capstone_slide_6.png",
    "/assets/slides/Capstone_slide_7.png",
    "/assets/slides/Capstone_slide_8.png",
]

def register_callbacks(app: Dash, df: pd.DataFrame):

    @app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
    )
    def render_content(tab):

        if tab == "tab-presentation":
            return html.Div(
                className="tab-panel",
                children=[
                    dcc.Store(id="slide-index", data=0),
                    html.Div(
                        [
                            html.Img(
                                id="slide-image",
                                src=slide_paths[0],
                                style={"width": "100%", "height": "auto"},
                            ),
                            html.Div(
                                [
                                    html.Button(
                                        "Previous",
                                        id="previous-slide",
                                        n_clicks=0,
                                    ),
                                    html.Span(
                                        f"Slide 1 of {len(slide_paths)}",
                                        id="slide-counter",
                                        style={"margin": "0 16px"},
                                    ),
                                    html.Button(
                                        "Next",
                                        id="next-slide",
                                        n_clicks=0,
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                    "marginTop": "12px",
                                },
                            ),
                        ],
                        style={"maxWidth": "1000px", "margin": "0 auto"},
                    ),
                ],
            )



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

        if tab == 'tab-sales-graphs':

            sales_locations_mapping = {
                'na_sales': 'North America',
                'jp_sales': 'Japan'
            }

            return html.Div(
                className='tab-panel',
                children=[
                    html.H3("Video Game Sales", className='tab-panel-title'),
                    create_game_sales_graph(sales_locations_mapping), 
                    create_game_sales_scatter(sales_locations_mapping=sales_locations_mapping)
                ]
            )

        if tab == 'tab-genre-graphs':

            genres = VideoGameSelectionOptions(df=df).genre_selection_options()

            return html.Div(
                className='tab-panel',
                children=[
                    html.H3("Sales by Genre", className='tab-panel-title'),
                    create_genres_region_graph(genres),
                    create_regions_genre_graph(genres=genres, regions=['North America', 'Japan']),
                    create_animated_sales_by_year_genre(regions_mapping=REGIONS_MAPPING)
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
                    html.H3("Sales by Platform", className='tab-panel-title'),
                    create_platforms_region_graph(platforms=all_platforms, regions_mapping=REGIONS_MAPPING),
                    create_animated_sales_by_year_platform(platforms=all_platforms, regions_mapping=REGIONS_MAPPING)
                ]
            )

        
        if tab == 'tab-publisher-graphs':

            publishers = VideoGameSelectionOptions(df=df).publisher_selection_options()

            return html.Div(
                className='tab-panel',
                children=[
                    html.H3("Sales by Publisher", className='tab-panel-title'),
                    create_publishers_region_graph(publishers=publishers, regions_mapping=REGIONS_MAPPING),
                ]
            )

        # if tab == 'tab-graph-pics':
        #     return html.Div([
        #         html.H3("Graphs", className='tab-panel-title'),
        #     ])

        # if tab == 'tab-resources':
        #     return html.Div([
        #         html.H3("Resources", className='tab-panel-title'),
        #     ])

    @app.callback(
        Output("slide-index", "data"),
        Input("previous-slide", "n_clicks"),
        Input("next-slide", "n_clicks"),
        State("slide-index", "data"),
        prevent_initial_call=True,
    )
    def change_slide(previous_clicks, next_clicks, index):
        from dash import ctx

        if ctx.triggered_id == "previous-slide":
            return max(0, index - 1)

        if ctx.triggered_id == "next-slide":
            return min(len(slide_paths) - 1, index + 1)

        return index


    @app.callback(
        Output("slide-image", "src"),
        Output("slide-counter", "children"),
        Output("previous-slide", "disabled"),
        Output("next-slide", "disabled"),
        Input("slide-index", "data"),
    )
    def display_slide(index):
        return (
            slide_paths[index],
            f"Slide {index + 1} of {len(slide_paths)}",
            index == 0,
            index == len(slide_paths) - 1,
        )
        
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

        update_graph_style2(fig)

        return fig

    @app.callback(
        Output('game-sales-scatter', 'figure'),
        Input('selected-scatter_regions-dropdown', 'value')
    )
    def update_sales_scatter(selected_regions):

        selected_regions = selected_regions or []

        region_columns = [
            REGION_COLUMNS[region]
            for region in (selected_regions or [])
            if region in REGION_COLUMNS
        ]

        if not region_columns:
            return px.scatter(title="Select at least one region.")

        missing = set(region_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Sales columns are missing from df: {missing}")

        yearly_sales = df.groupby('release_year', as_index=False)[region_columns].sum()

        plot_data = yearly_sales.melt(
            id_vars='release_year',
            value_vars=region_columns,
            var_name='region',
            value_name='sales'
        )

        column_to_region = {column: region for region, column in REGION_COLUMNS.items()}
        plot_data["region"] = plot_data["region"].map(column_to_region)

        fig = px.scatter(
            data_frame=plot_data,
            x='release_year',
            y='sales',
            color='region',
            labels={
                'release_year': 'Release Year',
                'sales': 'Sales',
                'region': 'Region'
            },
            title='Video Game Sales by Release Year'
        )

        update_graph_style2(fig)

        return fig

    update_genres_region_df = VideoGameDataFrames(df=df).sales_by_year_genre_df()


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

        data = update_genres_region_df[
            update_genres_region_df['genre'].isin(selected_genres)
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

        update_graph_style2(fig)

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

        data = update_genres_region_df[
            update_genres_region_df['genre'] == selected_genre
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

        update_graph_style2(fig)

        return fig

    update_publishers_region_df = VideoGameDataFrames(df=df).sales_by_year_publisher_df()

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

        data = update_publishers_region_df[
            update_publishers_region_df['publisher'].isin(selected_publishers)
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

        update_graph_style2(fig)

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

        update_graph_style2(fig)

        return fig

    update_animated_sales_by_year_genre_df = VideoGameDataFrames(df=df).animated_sales_by_year_genre_df()

    @app.callback(
        Output('genre-sales-animated', 'figure'),
        Input('selected-animated_region-dropdown', 'value')
    )
    def update_animated_sales_by_year_genre(selected_region):

        def max_range(df: pd.DataFrame, range_value: str):
            return df[range_value].max() * 1.1
        
        region_sales_column, region_sales_label = REGIONS_MAPPING.get(selected_region, (None, None))

        if selected_region not in REGIONS_MAPPING:
            return px.line(title="Select a valid sales region.")

        max_sales_range = max_range(df=update_animated_sales_by_year_genre_df, range_value=region_sales_column)

        fig = px.bar(
            data_frame=update_animated_sales_by_year_genre_df,
            x=region_sales_column,
            y='genre',
            color='genre',
            animation_frame='release_year',
            animation_group='genre',
            labels={
                region_sales_column: region_sales_label,
                'genre': 'Genre',
                'release_year': 'Release Year'
            },
            range_x=[0, max_sales_range]
        )

        fig.update_layout(
            xaxis_title=f"{selected_region} sales",
            yaxis_title="Genre"
        )

        update_graph_style2(fig)

        return fig

    animated_sales_by_year_platform_df = VideoGameDataFrames(df=df).animated_sales_by_year_platform_df()

    @app.callback(
        Output('platform-sales-animated', 'figure'),
        Input('selected-animated_platforms-dropdown', 'value'),
        Input('selected-pl_animated_region-dropdown', 'value'),
    )
    def update_animated_sales_by_year_platform(selected_platforms, selected_region):

        def max_range(df: pd.DataFrame, range_value: str):
            return df[range_value].max() * 1.1

        if not selected_platforms:
            return px.line(title="Select at least one platform/console.")

        if selected_region not in REGIONS_MAPPING:
            return px.line(title="Select a valid sales region.")
        
        region_sales_column, region_sales_label = REGIONS_MAPPING.get(selected_region, (None, None))

        data = animated_sales_by_year_platform_df[
            animated_sales_by_year_platform_df['platform_name'].isin(selected_platforms)
        ]

        max_sales_range = max_range(df=data, range_value=region_sales_column)

        fig = px.bar(
            data_frame=data,
            x=region_sales_column,
            y='platform_name',
            color='platform_name',
            animation_frame='release_year',
            animation_group='platform_name',
            labels={
                region_sales_column: region_sales_label,
                'platform_name': 'Gaming Platform',
                'release_year': 'Release Year'
            },
            range_x=[0, max_sales_range]
        )

        fig.update_layout(
            xaxis_title=region_sales_label,
            yaxis_title="Platform"
        )

        update_graph_style2(fig)

        return fig