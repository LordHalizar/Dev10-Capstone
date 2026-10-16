import pandas as pd
import pyspark.sql as sp
from pyspark.sql.functions import (
    col,
    round,
    year,
)
from pyspark.sql.types import (
    DateType,
    DoubleType,
    FloatType,
    IntegerType,
    StringType,
    TimestampType,
)


class BaseETLProcessor:
    def __init__(self, file_paths: list[str], df_column_mapping: dict[str, list[str]], db_columns: list[str]):
        self.file_paths = file_paths
        self.df_column_mapping = df_column_mapping
        self.db_columns = db_columns

    def raise_implement_error(self):
        raise NotImplementedError("Subclasses must implement the etl class for specific table types.")

    def matching_dataframe_datatypes(self, df1: sp.DataFrame, df2: sp.DataFrame) -> bool:
        return df1.dtypes == df2.dtypes

    def has_valid_join_columns(self, df: sp.DataFrame, join_columns: list[str]) -> bool:
        return all(column in df.columns for column in join_columns)

    def get_spark_datatype(self, df: sp.DataFrame, column: str):
        return df.schema[column].dataType

    def is_int(self, df: sp.DataFrame, column: str) -> bool:
        return isinstance(self.get_spark_datatype(df=df, column=column), IntegerType)

    def is_float(self, df: sp.DataFrame, column: str) -> bool:
        return isinstance(self.get_spark_datatype(df=df, column=column), (FloatType, DoubleType))

    def is_datetime(self, df: sp.DataFrame, column: str) -> bool:
        return isinstance(self.get_spark_datatype(df=df, column=column), (DateType, TimestampType))

    def is_string(self, df: sp.DataFrame, column: str) -> bool:
        return isinstance(self.get_spark_datatype(df=df, column=column), StringType)

    def extract(self, file_path: str, spark: sp.SparkSession) -> sp.DataFrame:
        if file_path.lower().endswith('.csv'):
            return spark.read.csv(path=file_path, header=True, inferSchema=True)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            pd_df = pd.read_excel(file_path)
            return spark.createDataFrame(pd_df)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")


    def transform(self, df: sp.DataFrame, df_columns: list[str]) -> sp.DataFrame:
        if not df_columns or not self.db_columns:
            raise ValueError("Source and database column lists must not be empty.")

        if len(df_columns) != len(self.db_columns):
            raise ValueError("The number of source columns must equal the number of database columns.")

        missing = [column for column in df_columns if column not in df.columns]
        if missing:
            raise ValueError(f"Source DataFrame is missing columns: {missing}")
        
        df = df.select(*[col(source).alias(target) for source, target in zip(df_columns, self.db_columns)])
        df = df.na.replace('', None, subset=self.db_columns)
        df = df.dropna(subset=self.db_columns).dropDuplicates()
        return df
        

    def load(self, df: sp.DataFrame, spark: sp.SparkSession, table: str):
        try:
            jdbc_options = {
                "url": spark.conf.get("spark.postgresql.video_games.url"),
                "user": spark.conf.get("spark.postgresql.video_games.user"),
                "password": spark.conf.get("spark.postgresql.video_games.password"),
                "driver": "org.postgresql.Driver",
            }

            df.write.format("jdbc").options(**jdbc_options, dbtable=table).mode(
                "append"
            ).save()
        except Exception as e:
            print(f"[ERR]: AN error occurred while loading data: {e}")
            raise

    def process(self, table: str):

        spark = sp.SparkSession.builder.appName(f'{table}ETL').getOrCreate()

        try:
            if not self.file_paths:
                raise ValueError("No file paths were provided.")

            if len(self.file_paths) != len(self.df_column_mapping):
                raise ValueError("TThe number of files paths must match the number of column mappings.")

            transformed_dfs = []

            for file_path in self.file_paths:
                if file_path not in self.df_column_mapping:
                    raise ValueError(f"No column mapping provided for {file_path}")

                df_columns = self.df_column_mapping[file_path]

                print(f"Extracting data from [{file_path}] for {table} table...")
                extracted_df = self.extract(file_path=file_path, spark=spark)

                print(f"Transforming data from [{file_path}] for {table} table...")
                transformed_df = self.transform(df=extracted_df, df_columns=df_columns)
                transformed_dfs.append(transformed_df)

            combined_df = transformed_dfs[0]

            for df in transformed_dfs[1:]:
                if not self.matching_dataframe_datatypes(combined_df, df):
                    raise ValueError("Miss matched column datatypes. Unable to merge.")
                
                combined_df = combined_df.unionByName(df)

            combined_df = combined_df.dropDuplicates()

            print(f"Loading {table} table data...")
            self.load(df=combined_df, spark=spark, table=table)
            print(f"{table.title()} table data loaded successfully!")
        
        except Exception as e:
            print(f"[ERR]: An unexpected error occurred: {e}")
            raise
        
        finally:
            print(f"Stopping Spark session for {table} table.")
            spark.stop()

# Completely uses base class. No additional functionality needed.
class GenreETLProcessor(BaseETLProcessor):
    pass

# Completely uses base class. No additional functionality needed.
class PublisherETLProcessor(BaseETLProcessor):
    pass

class GameETLProcessor(BaseETLProcessor):
    def __init__(self, file_paths: list[str], df_column_mapping: dict[str, list[str]], db_columns: list[str], lookups: list[dict[str, str]]):
        super().__init__(file_paths, df_column_mapping, db_columns)

        self.lookups = lookups

    def extract_foreign_keys(self, table: str, spark: sp.SparkSession) -> sp.DataFrame:
        jdbc_options = {
            "url": spark.conf.get("spark.postgresql.video_games.url"),
            "user": spark.conf.get("spark.postgresql.video_games.user"),
            "password": spark.conf.get("spark.postgresql.video_games.password"),
            "driver": "org.postgresql.Driver",
        }

        df = spark.read.format('jdbc').options(**jdbc_options, dbtable=table).load()

        return df

    def convert_release_year(self, df: sp.DataFrame, year_column: str):
        if self.is_int(df=df, column=year_column):
            return df
        elif self.is_float(df=df, column=year_column):
            return df.withColumn(year_column, round(col(year_column), 0).cast('int'))
        elif self.is_string(df=df, column=year_column):
            return df.withColumn(year_column, round(col(year_column).cast('double')).cast('int'))
        elif self.is_datetime(df=df, column=year_column):
            return df.withColumn(year_column, year(col(year_column)).cast('int'))
        else:
            raise ValueError(
                f"Unsupported Spark datatype for column {year_column}: "
                f"{self.get_spark_datatype(df=df, column=year_column)}"
            )


    def transform(self, df: sp.DataFrame, df_columns: list[str]) -> sp.DataFrame:
        if not df_columns or not self.db_columns:
            raise ValueError("Source and database column lists must not be empty.")

        if len(df_columns) != len(self.db_columns):
            raise ValueError("The number of source columns must equal the number of database columns.")

        missing = [column for column in df_columns if column not in df.columns]
        if missing:
            raise ValueError(f"Source DataFrame is missing columns: {missing}")
        
        df = df.select(*[col(source).alias(target) for source, target in zip(df_columns, self.db_columns)])
        df = df.na.replace('', None, subset=self.db_columns)
        df = df.dropna(subset=self.db_columns).dropDuplicates(subset=self.db_columns)

        try:
            if 'release_year' in df.columns:
                df = self.convert_release_year(df=df, year_column='release_year')
        except Exception as e:
            print(f"[ERR] An error occurred when attempting to convert release_value: {e}")
            raise

        return df.drop()
    
    def transform_foreign_keys(self, df: sp.DataFrame, join_key: str, foreign_key: str) -> sp.DataFrame:

        columns = [join_key, foreign_key]
        missing = [column for column in columns if column not in df.columns]

        if missing:
            raise ValueError(f"Lookup DataFrame is missing columns: {missing}")

        return (
            df.select(*columns)
            .na.replace('', None, subset=columns)
            .dropna(subset=columns)
            .dropDuplicates(columns)
        )

    # Needs work
    def process(self, table: str):
        spark = sp.SparkSession.builder.appName(f'{table}ETL').getOrCreate()

        try:
            transformed_dfs = []

            for file_path in self.file_paths:
                if file_path not in self.df_column_mapping:
                    raise ValueError(f"No column mapping provided for {file_path}")

                df_columns = self.df_column_mapping[file_path]

                print(f"Extracting data from [{file_path}] for {table} table...")
                extracted_df = self.extract(file_path=file_path, spark=spark)

                print(f"Transforming data from [{file_path}] for {table} table...")
                transformed_df = self.transform(df=extracted_df, df_columns=df_columns)
                transformed_dfs.append(transformed_df)

            if not transformed_dfs:
                raise ValueError("No file paths were provided.")

            combined_df = transformed_dfs[0]


            for df in transformed_dfs[1:]:
                if not self.matching_dataframe_datatypes(combined_df, df):
                    raise ValueError("Mismatched column datatypes. Unable to merge.")

                if combined_df.columns != df.columns:
                    raise ValueError(
                        "Mismatched column names or order. Unable to merge.\n"
                        f"combined_df columns: {combined_df.columns}\n"
                        f"df columns: {df.columns}"
                    )

                combined_df = combined_df.unionByName(df)

            combined_df = combined_df.dropDuplicates(self.db_columns).dropna(how='any')

            for config in self.lookups:
                lookup_df = self.extract_foreign_keys(
                    table=config['table'],
                    spark=spark
                )

                join_key = config['join_key']
                foreign_key = config['foreign_key']

                lookup = (lookup_df.select(join_key, foreign_key))

                combined_df = (
                    combined_df.join(
                        lookup, 
                        on=join_key, 
                        how='inner'
                    )
                    .drop(join_key)
                )

            final_df = combined_df.dropDuplicates(subset=['game_title', 'release_year', 'genre_id', 'publisher_id'])

            print(f"Loading {table} table data...")
            self.load(df=final_df, spark=spark, table=table)
            print(f"{table.title()} table data loaded successfully!")
        
        except Exception as e:
            print(f"[ERR]: An unexpected error occurred: {e}")
            final_df.write.csv('/opt/spark/files/out/csv/failed_game_table_data_upload', header=True, mode='overwrite')
            raise
        
        finally:
            print(f"Processing for {table} table completed.")
            spark.stop()

# Completely uses base class. No additional functionality needed.
class PlatformETLProcessor(BaseETLProcessor):
    pass

class GamePlatformETLProcessor(BaseETLProcessor):
    pass

class SalesETLProcessor(BaseETLProcessor):
    pass
