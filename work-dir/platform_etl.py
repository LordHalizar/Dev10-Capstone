from etl import PlatformETLProcessor

CSV_FILE_PATH = "/opt/spark/files/in/csv/Video_Games.csv"
EXCEL_FILE_PATH = "/opt/spark/files/in/excel/VideoGames_Sales.xlsx"

FILE_PATHS = [CSV_FILE_PATH, EXCEL_FILE_PATH]

DF_COLUMN_MAPPING = {
    CSV_FILE_PATH: ['Platform'],
    EXCEL_FILE_PATH: ['console']
}

platform_etl = PlatformETLProcessor(file_paths=FILE_PATHS, df_column_mapping=DF_COLUMN_MAPPING, db_columns=['platform_name'])
platform_etl.process(table='platform')