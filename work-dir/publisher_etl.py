from etl import PublisherETLProcessor

CSV_FILE_PATH = "/opt/spark/files/in/csv/Video_Games.csv"
EXCEL_FILE_PATH = "/opt/spark/files/in/excel/VideoGames_Sales.xlsx"

FILE_PATHS = [CSV_FILE_PATH, EXCEL_FILE_PATH]

DF_COLUMN_MAPPING = {
    CSV_FILE_PATH: ['Publisher'],
    EXCEL_FILE_PATH: ['publisher']
}

publisher_etl = PublisherETLProcessor(file_paths=FILE_PATHS, df_column_mapping=DF_COLUMN_MAPPING, db_columns=['publisher_name'])
publisher_etl.process(table='publisher')