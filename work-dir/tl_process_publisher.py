import pyspark.sql as sp
from etl import PublisherTLProcessor


def publisher_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    publisher_tl = PublisherTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark)
    publisher_tl.process(table='publisher')