import pyspark.sql as sp
from etl import ETProcessor, GamePlatformTLProcessor

CSV_FILE_PATH = "/opt/spark/files/in/csv/Video_Games.csv"
EXCEL_FILE_PATH = "/opt/spark/files/in/excel/VideoGames_Sales.xlsx"

FILE_PATHS = [CSV_FILE_PATH, EXCEL_FILE_PATH]

DF_COLUMN_MAPPING = {
    CSV_FILE_PATH: ['Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'NA_Sales', 'JP_Sales'],
    EXCEL_FILE_PATH: ['title', 'console', 'release_date', 'genre', 'publisher', 'na_sales(mil)', 'jp_sales(mil)']
}

DB_COLUMNS = ['game_title', 'platform_name', 'release_year', 'genre_name', 'publisher_name', 'na_sales', 'jp_sales']

UNIQUE_RECORD_KEYS = ['game_title', 'platform_name', 'publisher_name']

LOOKUP_MAPPING = [
    {
        'table': 'game',
        'join_key': 'game_title',
        'foreign_key': 'game_id'
    },
    {
        'table': 'platform',
        'join_key': 'platform_name',
        'foreign_key': 'platform_id'
    }
]

spark = sp.SparkSession.builder.appName('GenreETL').getOrCreate()

source_process = ETProcessor(file_paths=FILE_PATHS, df_column_mapping=DF_COLUMN_MAPPING, db_columns=DB_COLUMNS, spark=spark, unique_records_keys=UNIQUE_RECORD_KEYS)
source_df = source_process.process()
game_platform_etl = GamePlatformTLProcessor(source_df=source_df, db_columns=['game_id', 'platform_id'], spark=spark, lookups=LOOKUP_MAPPING)
game_platform_etl.process(table='game_platform')

spark.stop()