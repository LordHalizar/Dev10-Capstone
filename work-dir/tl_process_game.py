import pyspark.sql as sp
from etl import GameTLProcessor


def game_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    game_tl = GameTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark)
    game_tl.process(table='game')