import plotly.express as px

from dash import dcc, html

def update_graph_style1(fig):
    return fig.update_layout(
        title={
            'text': "Game Sales by Region",
            'x': 0.5,                   # center title
            'xanchor': "center",
            'font': {
                'family': "Arial, sans-serif",
                'size': 23,
                'color': "black",
            },
            # Green title bar, similar to your Data Table heading
            'pad': {'t': 10, 'b': 10},
        },

        # Axis labels and tick labels
        xaxis={
            'title': {
                'font': {'family': "Arial, sans-serif", 'size': 15, 'color': "#123047"}
            },
            'tickfont': {'family': "Arial, sans-serif", 'size': 12, 'color': "#123047"},
        },
        yaxis={
            'title': {
                'font': {'family': "Arial, sans-serif", 'size': 15, 'color': "#123047"}
            },
            'tickfont': {'family': "Arial, sans-serif", 'size': 12, 'color': "#123047"},
        },

        legend={
            'font': {'family': "Arial, sans-serif", 'size': 12, 'color': "#123047"},
        },
    )

def update_graph_style2(fig):
    return fig.update_layout(
        template="plotly_white",
        font={
            'family': "Arial, sans-serif",
            'size': 12,
            'color': "#263238",
        },
        title={
            'font': {'size': 18, 'color': "#263238"},
            'x': 0.02,
            'xanchor': "left",
        },
        margin={'l': 45, 'r': 25, 't': 55, 'b': 45},
        legend={
            'font': {'size': 11, 'color': "#263238"},
            'bgcolor': "rgba(255,255,255,0.8)",
            'borderwidth': 0,
        },
        xaxis={
            'title_font': {'size': 13, 'color': "#263238"},
            'tickfont': {'size': 11, 'color': "#64716d"},
            'showgrid': False,
            'zeroline': False,
            'linecolor': "#e5eae8",
        },
        yaxis={
            'title_font': {'size': 13, 'color': "#263238"},
            'tickfont': {'size': 11, 'color': "#64716d"},
            'gridcolor': "#edf1ef",
            'zeroline': False,
        },
    )

def create_game_sales_graph(sales_locations_mapping: dict[str, str]) -> html.Div:

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-sales_regions-dropdown',
                options=[
                    {'label': location, 'value': location} for location in sales_locations_mapping.values()
                ],
                value=list(sales_locations_mapping.values()),
                multi=True,
                placeholder='Select sales regions',
                className='dashboard-dropdown'
            ),
            dcc.Graph(
                id='game-sales-graph',
                className='tab-graph'
            ),
        ]
    )

def create_game_sales_scatter(sales_locations_mapping: dict[str, str]) -> html.Div:

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-scatter_regions-dropdown',
                options=[
                    {'label': location, 'value': location} for location in sales_locations_mapping.values()
                ],
                value=list(sales_locations_mapping.values()),
                multi=True,
                placeholder='Select sales regions'
            ),
            dcc.Graph(
                id='game-sales-scatter',
                className='tab-graph'
            ),
        ]
    )

def create_genres_region_graph(genres: list[str]) -> html.Div:

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

def create_regions_genre_graph(genres: list[str], regions: list[str]) -> html.Div:
    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-genre-dropdown',
                options=[
                    {'label': genre, 'value': genre} for genre in genres
                ],
                value=genres[0],
                multi=False,
                placeholder='Selected genre'
            ),
            dcc.Dropdown(
                id='selected-regions-dropdown',
                options=[
                    {'label': region, 'value': region} for region in regions
                ],
                value=regions,
                multi=True,
                placeholder='Selected Regions'
            ),
            dcc.Graph(id='regions-genre-graph'),
        ]
    )

def create_publishers_region_graph(publishers: list[str], regions_mapping: dict[str, tuple[str, str]]) -> html.Div:
    region_keys = list(regions_mapping.keys())

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-R_publishers-dropdown',
                options=[
                    {'label': publisher, 'value': publisher} for publisher in publishers
                ],
                value=publishers,
                multi=True,
                placeholder='Select publishers'
            ),
            dcc.Dropdown(
                id='selected-P_region-dropdown',
                options=[
                    {'label': region, 'value': region} for region in regions_mapping
                ],
                multi=False,
                value=region_keys[0] if region_keys else None,
                clearable=False
            ),
            dcc.Graph(id='publishers-region-graph'),
        ]
    )

def create_platforms_region_graph(platforms: list[str], regions_mapping: dict[str, tuple[str, str]]) -> html.Div:
    region_keys = list(regions_mapping.keys())

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-platforms-dropdown',
                options=[
                    {'label': platform, 'value': platform} for platform in platforms
                ],
                value=platforms,
                multi=True,
                placeholder='Select Platforms'
            ),
            dcc.Dropdown(
                id='selected-Pl_region-dropdown',
                options=[
                    {'label': region, 'value': region} for region in regions_mapping
                ],
                multi=False,
                value=region_keys[0] if region_keys else None,
                clearable=False
            ),
            dcc.Graph(id='platforms-region-graph'),
        ]
    )

def create_animated_sales_by_year_genre(regions_mapping: dict[str, tuple[str, str]]) -> html.Div:
    regions = list(regions_mapping.keys())

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-animated_region-dropdown',
                options=[
                    {'label': region, 'value': region} for region in regions
                ],
                multi=False,
                value=regions[0] if regions else None,
                clearable=False
            ),
            dcc.Graph(id='genre-sales-animated'),
        ]
    )

displayed_platforms = ['Atari 2600', 'NES', 'SNES', 'GameBoy', 'GameBoy Advance', 'Nintendo 3DS', 'Nintendo 64', 'Nintendo GameCube', 'Nintendo Wii', 'PC', 'Playstation Portable', 'Playstation Vita', 'PS1', 'PS2', 'PS3', 'PS4']

def create_animated_sales_by_year_platform(platforms: list[str], regions_mapping: dict[str, tuple[str, str]]) -> html.Div:
    regions = list(regions_mapping.keys())

    return html.Div(
        className='tab-panel',
        children=[
            dcc.Dropdown(
                id='selected-animated_platforms-dropdown',
                options=[
                    {'label': platform, 'value': platform} for platform in platforms
                ],
                value=platforms,
                multi=True,
                placeholder='Select Platforms'
            ),
            dcc.Dropdown(
                id='selected-pl_animated_region-dropdown',
                options=[
                    {'label': region, 'value': region} for region in regions
                ],
                multi=False,
                value=regions[0] if regions else None,
                clearable=False
            ),
            dcc.Graph(id='platform-sales-animated'),
        ]
    )