import plotly.express as px

from dash import dcc, html


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
                placeholder='Select sales regions'
            ),
            dcc.Graph(id='game-sales-graph'),
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
            dcc.Graph(id='game-sales-scatter'),
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