import pyspark.sql as sp
from etl import ETProcessor

VIDEO_GAMES_CSV_FILE_PATH = "/opt/spark/files/in/csv/Video_Games.csv"
# VGCHARTZ_2024_CSV_FILE_PATH = "/opt/spark/files/in/csv/vgchartz-2024.csv"
VGSALES_CSV_FILE_PATH = "/opt/spark/files/in/csv/vgsales.csv"

# VIDEO_GAMES_SALES_EXCEL_FILE_PATH = "/opt/spark/files/in/excel/VideoGames_Sales.xlsx"

FILE_PATHS = [
    VIDEO_GAMES_CSV_FILE_PATH, 
    # VGCHARTZ_2024_CSV_FILE_PATH, 
    VGSALES_CSV_FILE_PATH,
    # VIDEO_GAMES_SALES_EXCEL_FILE_PATH
]

DF_COLUMN_MAPPING = {
    VIDEO_GAMES_CSV_FILE_PATH: ['Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'NA_Sales', 'JP_Sales'],
    # VGCHARTZ_2024_CSV_FILE_PATH: ['title', 'console', 'release_date', 'genre', 'publisher', 'na_sales', 'jp_sales'],
    VGSALES_CSV_FILE_PATH: ['Name', 'Platform', 'Year', 'Genre', 'Publisher', 'NA_Sales', 'JP_Sales'],
    # VIDEO_GAMES_SALES_EXCEL_FILE_PATH: ['title', 'console', 'release_date', 'genre', 'publisher', 'na_sales(mil)', 'jp_sales(mil)']
}

DB_COLUMNS = ['game_title', 'platform_name', 'release_year', 'genre_name', 'publisher_name', 'na_sales', 'jp_sales']

UNIQUE_RECORD_KEYS = ['game_title', 'platform_name', 'publisher_name']

SUFFIX_FILTER_MAPPING = {'game_title': [' sales)']}

REPLACE_MAPPING = {
    'platform_name': {
        '2600': 'Atari 2600', 
        'GB':'GameBoy', 
        'GBA': 'GameBoy Advance', 
        'SCD': 'Sega CD', 
        'SAT': 'Sega Saturn', 
        '3DO': '3DO Interactive Multiplayer', 
        'GEN': 'Sega Genesis', 
        'PS': 'PS1', 
        'NG': 'Neo Geo', 
        'N64': 'Nintendo 64', 
        'DC': 'Sega Dreamcast', 
        'WS': 'Bandia WonderSwan',
        'GC': 'Nintendo GameCube',
        'XB': 'Xbox',
        'PSP': 'Playstation Portable',
        'DS': 'Nintendo DS',
        'Wii': 'Nintendo Wii',
        'X360': 'Xbox 360',
        '3DS': 'Nintendo 3DS',
        'PSV': "Playstation Vita",
        'XOne': "Xbox One"
    }
}

def et_process(spark: sp.SparkSession):
    source_process = ETProcessor(file_paths=FILE_PATHS, df_column_mapping=DF_COLUMN_MAPPING, db_columns=DB_COLUMNS, spark=spark, unique_records_keys=UNIQUE_RECORD_KEYS, suffix_filter_mapping=SUFFIX_FILTER_MAPPING, replace_filter_mapping=REPLACE_MAPPING)
    source_df = source_process.process()
    return source_df