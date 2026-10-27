import pyspark.sql as sp
from etl import GamePublisherTLProcessor

LOOKUP_MAPPING = [
    {
        'table': 'game',
        'join_key': 'game_title',
        'foreign_key': 'game_id'
    },
    {
        'table': 'publisher',
        'join_key': 'publisher_name',
        'foreign_key': 'publisher_id'
    }
]

def game_publisher_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    game_publisher_tl = GamePublisherTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark, lookups=LOOKUP_MAPPING)
    game_publisher_tl.process(table='game_publisher')