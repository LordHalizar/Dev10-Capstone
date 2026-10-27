import pyspark.sql as sp
from etl import SalesTLProcessor

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
    },
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
    },
    {
        'table': 'game_platform_release',
        'join_key': 'game_platform_id',
        'foreign_key': 'game_platform_release_id'
    }
]

def sales_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    sales_tl = SalesTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark, lookups=LOOKUP_MAPPING)
    sales_tl.process(table='sales')