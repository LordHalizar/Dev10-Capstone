import pyspark.sql as sp
from etl import GamePlatformTLProcessor

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

def game_platform_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    game_platform_tl = GamePlatformTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark, lookups=LOOKUP_MAPPING)
    game_platform_tl.process(table='game_platform')