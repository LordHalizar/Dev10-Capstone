import pyspark.sql as sp
from etl import PlatformTLProcessor


def platform_tl(source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
    platform_tl = PlatformTLProcessor(source_df=source_df, db_columns=db_columns, spark=spark)
    platform_tl.process(table='platform')