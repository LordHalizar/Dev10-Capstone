import pyspark.sql as sp
from etl import GameTLProcessor

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

def game_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    game_tl = GameTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark, lookups=LOOKUP_MAPPING)
    game_tl.process(table='game')