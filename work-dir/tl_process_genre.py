import pyspark.sql as sp
from etl import GenreTLProcessor


def genre_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    genre_tl = GenreTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark)
    genre_tl.process(table='genre')