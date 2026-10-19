import pyspark.sql as sp
from etl import ETProcessor

VIDEO_GAMES_CSV_FILE_PATH = "/opt/spark/files/in/csv/Video_Games.csv"
VGCHARTZ_2024_CSV_FILE_PATH = "/opt/spark/files/in/csv/vgchartz-2024.csv"
VIDEO_GAMES_SALES_EXCEL_FILE_PATH = "/opt/spark/files/in/excel/VideoGames_Sales.xlsx"

FILE_PATHS = [
    VIDEO_GAMES_CSV_FILE_PATH, 
    VGCHARTZ_2024_CSV_FILE_PATH, 
    VIDEO_GAMES_SALES_EXCEL_FILE_PATH
]

DF_COLUMN_MAPPING = {
    VIDEO_GAMES_CSV_FILE_PATH: ['Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'NA_Sales', 'JP_Sales'],
    VGCHARTZ_2024_CSV_FILE_PATH: ['title', 'console', 'release_date', 'genre', 'publisher', 'na_sales', 'jp_sales'],
    VIDEO_GAMES_SALES_EXCEL_FILE_PATH: ['title', 'console', 'release_date', 'genre', 'publisher', 'na_sales(mil)', 'jp_sales(mil)']
}

DB_COLUMNS = ['game_title', 'platform_name', 'release_year', 'genre_name', 'publisher_name', 'na_sales', 'jp_sales']

UNIQUE_RECORD_KEYS = ['game_title', 'platform_name', 'publisher_name']

def et_process(spark: sp.SparkSession):
    source_process = ETProcessor(file_paths=FILE_PATHS, df_column_mapping=DF_COLUMN_MAPPING, db_columns=DB_COLUMNS, spark=spark, unique_records_keys=UNIQUE_RECORD_KEYS)
    source_df = source_process.process()
    return source_df