from etl import GameETLProcessor

CSV_FILE_PATH = "/opt/spark/files/in/csv/Video_Games.csv"
EXCEL_FILE_PATH = "/opt/spark/files/in/excel/VideoGames_Sales.xlsx"

FILE_PATHS = [CSV_FILE_PATH, EXCEL_FILE_PATH]

DF_COLUMN_MAPPING = {
    CSV_FILE_PATH: ['Name', 'Year_of_Release', 'Genre', 'Publisher'],
    EXCEL_FILE_PATH: ['title', 'release_date', 'genre', 'publisher']
}

LOOKUP_MAPPING = [
    {
        'table': 'genre',
        'join_key': 'genre_name',
        'foreign_key': 'genre_id'
    },
    {
        'table': 'publisher',
        'join_key': 'publisher_name',
        'foreign_key': 'publisher_id'
    }
]

game_etl = GameETLProcessor(file_paths=FILE_PATHS, df_column_mapping=DF_COLUMN_MAPPING, db_columns=['game_title', 'release_year', 'genre_name', 'publisher_name'], lookups=LOOKUP_MAPPING)
game_etl.process(table='game')