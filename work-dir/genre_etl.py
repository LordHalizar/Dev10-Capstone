from etl import GenreETLProcessor

CSV_FILE_PATH = "/opt/spark/files/in/csv/Video_Games.csv"
EXCEL_FILE_PATH = "/opt/spark/files/in/excel/VideoGames_Sales.xlsx"

FILE_PATHS = [CSV_FILE_PATH, EXCEL_FILE_PATH]

DF_COLUMN_MAPPING = {
    CSV_FILE_PATH: ['Genre'],
    EXCEL_FILE_PATH: ['genre']
}

genre_etl = GenreETLProcessor(file_paths=FILE_PATHS, df_column_mapping=DF_COLUMN_MAPPING, db_columns=['genre_name'])
genre_etl.process(table='genre')