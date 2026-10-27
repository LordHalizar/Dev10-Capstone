import pyspark.sql as sp
from etl import GameGenreTLProcessor

LOOKUP_MAPPING = [
    {
        'table': 'game',
        'join_key': 'game_title',
        'foreign_key': 'game_id'
    },
    {
        'table': 'genre',
        'join_key': 'genre_name',
        'foreign_key': 'genre_id'
    }
]

def game_genre_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    game_genre_tl = GameGenreTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark, lookups=LOOKUP_MAPPING)
    game_genre_tl.process(table='game_genre')