import pyspark.sql as sp
from etl import GamePlatformReleaseTLProcessor

LOOKUP_MAPPING = [
    {
        'table': 'game',
        'join_key': 'game_title',
        'foreign_key': 'game_id'
    },
    {
        'table': 'platform',
        'join_key': 'platform_name',
        'foreign_key': 'platform_id',
    },
    {
        'table': 'game_platform',
        'join_key': ['game_id', 'platform_id'],
        'foreign_key': 'game_platform_id'
    }
]

def game_platform_release_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    game_platform_release_tl = GamePlatformReleaseTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark, lookups=LOOKUP_MAPPING)
    game_platform_release_tl.process(table='game_platform_release')