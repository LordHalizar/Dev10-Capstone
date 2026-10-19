import pandas as pd
import pyspark.sql as sp
from pyspark.sql.functions import (
    col,
    round,
    trim,
    when,
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


class ETProcessor:
    def __init__(self, file_paths: list[str], df_column_mapping: dict[str, list[str]], db_columns: list[str], spark: sp.SparkSession, unique_records_keys: list[str] | None = None):
        self.file_paths = file_paths
        self.df_column_mapping = df_column_mapping
        self.db_columns = db_columns
        self.unique_records_keys = unique_records_keys
        self.spark = spark

    def matching_dataframe_datatypes(self, df1: sp.DataFrame, df2: sp.DataFrame) -> bool:
        return df1.dtypes == df2.dtypes

    def extract(self, file_path: str) -> sp.DataFrame:
        if file_path.lower().endswith('.csv'):
            return self.spark.read.csv(path=file_path, header=True, inferSchema=True)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            pd_df = pd.read_excel(file_path)
            return self.spark.createDataFrame(pd_df)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

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

    def _validate_columns(self, df: sp.DataFrame, required_columns: list[str], context: str):
        missing = [column for column in required_columns if column not in df.columns]
        if missing:
            raise ValueError(f"{context} is missing the following columns: {missing}")

    def transform(self, df: sp.DataFrame, df_columns: list[str]) -> sp.DataFrame:
        if not df_columns or not self.db_columns:
            raise ValueError("Source and database column lists must not be empty.")

        if len(df_columns) != len(self.db_columns):
            raise ValueError("The number of source columns must equal the number of database columns.")

        self._validate_columns(df=df, required_columns=df_columns, context="Source DataFrame")
        
        df = df.select(*[col(source).alias(target) for source, target in zip(df_columns, self.db_columns)])

        for name, dtype in df.dtypes:
            if dtype == 'string':
                df = df.withColumn(
                    name,
                    when(trim(col(name)) == '', None).otherwise(trim(col(name)))
                )

        if 'release_year' in df.columns:
            try:
                df = self.convert_release_year(df=df, year_column='release_year')
            except Exception as e:
                print(f"[ERR] An error occurred when attempting to convert release_year: {e}")
                raise

        keys = self.unique_records_keys or self.db_columns
        self._validate_columns(df=df, required_columns=keys, context="Uniqueness-key")

        df = df.dropna(subset=self.db_columns).dropDuplicates(subset=keys)
        return df

    def process(self):

        if not self.file_paths:
            raise ValueError("No file paths were provided.")

        if set(self.file_paths) != set(self.df_column_mapping):
            raise ValueError("Files paths and mapping keys must match exactly.")

        transformed_dfs = []

        try:
            for file_path in self.file_paths:
                df_columns = self.df_column_mapping[file_path]

                print(f"Extracting data from [{file_path}] for database...")
                extracted_df = self.extract(file_path=file_path)

                print(f"Transforming data from [{file_path}] for database...")
                transformed_df = self.transform(df=extracted_df, df_columns=df_columns)
                transformed_dfs.append(transformed_df)

            combined_df = transformed_dfs[0]

            for df in transformed_dfs[1:]:
                if not self.matching_dataframe_datatypes(df1=combined_df, df2=df):
                    raise ValueError("Column names or data types do not match; Unable to merge.")
                
                combined_df = combined_df.unionByName(df)

            return combined_df.dropDuplicates()
        
        except Exception as e:
            print(f"[ERR]: An unexpected error occurred: {e}")
            raise

class BaseTLProcessor:
    def __init__(self, source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession):
        self.source_df = source_df
        self.db_columns = db_columns
        self.spark = spark

    def raise_implement_error(self):
        raise NotImplementedError("Subclasses must implement the etl class for specific table types.")

    def has_valid_join_columns(self, df: sp.DataFrame, join_columns: list[str]) -> bool:
        return all(column in df.columns for column in join_columns)

    def extract_foreign_keys(self, table: str) -> sp.DataFrame:
        jdbc_options = {
            "url": self.spark.conf.get("spark.postgresql.video_games.url"),
            "user": self.spark.conf.get("spark.postgresql.video_games.user"),
            "password": self.spark.conf.get("spark.postgresql.video_games.password"),
            "driver": "org.postgresql.Driver",
        }

        df = self.spark.read.format('jdbc').options(**jdbc_options, dbtable=table).load()

        return df

    def transform(self, df: sp.DataFrame) -> sp.DataFrame:
        if not self.db_columns:
            raise ValueError("Database column list must not be empty.")

        missing = [column for column in self.db_columns if column not in df.columns]
        if missing:
            raise ValueError(f"Source DataFrame is missing columns: {missing}")
        
        df = df.select(*self.db_columns)
        df = df.na.replace('', None, subset=self.db_columns)
        df = df.dropna(subset=self.db_columns, how='all').dropDuplicates()
        return df

    def transform_foreign_keys(self, df: sp.DataFrame, join_key: str | list[str], foreign_key: str) -> sp.DataFrame:

        join_keys = [join_key] if isinstance(join_key, str) else join_key

        columns = [*join_keys, foreign_key]
        missing = [column for column in columns if column not in df.columns]

        if missing:
            raise ValueError(f"Lookup DataFrame is missing columns: {missing}")

        return (
            df.select(*columns)
            .na.replace('', None, subset=columns)
            .dropna(subset=columns)
            .dropDuplicates(columns)
        )

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

    def process_foreign_keys(self, df: sp.DataFrame, lookups):
            for config in lookups:
                lookup_df = self.extract_foreign_keys(table=config['table'])

                lookup = self.transform_foreign_keys(
                    df=lookup_df,
                    join_key=config['join_key'],
                    foreign_key=config['foreign_key']
                )

                df = (
                    df.join(
                        lookup, 
                        on=config['join_key'], 
                        how='inner'
                    )
                    .drop(config['join_key'])
                )

            return df.dropDuplicates()

    def fetch_foreign_keys(self, df: sp.DataFrame, lookups: list[dict]) -> sp.DataFrame:
            for config in lookups:
                table = config.get('table')
                join_keys = config.get('join_key')
                foreign_key = config.get('foreign_key')
                drop_keys = config.get('drop_key')
                join_type = config.get('join_type', 'inner')

                if isinstance(join_keys, str):
                    join_keys = [join_keys]

                if isinstance(drop_keys, str):
                    drop_keys = [drop_keys]

                lookup_df = self.extract_foreign_keys(table=table)

                lookup = self.transform_foreign_keys(
                    df=lookup_df,
                    join_key=join_keys,
                    foreign_key=foreign_key
                )

                df = (
                    df.join(
                        lookup, 
                        on=join_keys, 
                        how=join_type
                    )
                )

                if drop_keys is not None:
                    df = df.drop(drop_keys)

            return df.dropDuplicates()

    def process(self, table: str):
        try:
            if self.source_df is None:
                raise ValueError("No source DataFrame was provided")

            print(f"Transforming data from for {table} table...")
            transformed_df = self.transform(df=self.source_df)

            print(f"Loading {table} table data...")
            self.load(df=transformed_df, spark=self.spark, table=table)
            print(f"{table.title()} table data loaded successfully!")
        
        except Exception as e:
            print(f"[ERR]: An unexpected error occurred: {e}")
            raise

# Completely uses base class. No additional functionality needed.
class GenreTLProcessor(BaseTLProcessor):
    pass

# Completely uses base class. No additional functionality needed.
class PublisherTLProcessor(BaseTLProcessor):
    pass

class GameTLProcessor(BaseTLProcessor):
    def __init__(self, source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession, lookups: list[dict[str, str]]):
        super().__init__(source_df, db_columns, spark)

        self.lookups = lookups

    def process(self, table: str):
        try:
            if self.source_df is None:
                raise ValueError("No source DataFrame was provided")

            combined_df = self.fetch_foreign_keys(df=self.source_df, lookups=self.lookups)

            print(f"Transforming data from for {table} table...")
            transformed_df = self.transform(df=combined_df)

            final_df = transformed_df.dropDuplicates(subset=self.db_columns).dropna(how='any')    

            print(f"Loading {table} table data...")
            self.load(df=final_df, spark=self.spark, table=table)
            print(f"{table.title()} table data loaded successfully!")
        
        except Exception as e:
            print(f"[ERR]: An unexpected error occurred: {e}")
            raise

# Completely uses base class. No additional functionality needed.
class PlatformTLProcessor(BaseTLProcessor):
    pass

class GamePlatformTLProcessor(BaseTLProcessor):
    def __init__(self, source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession, lookups: list[dict[str, str]]):
        super().__init__(source_df, db_columns, spark)

        self.lookups = lookups

    def process(self, table: str):
        try:
            if self.source_df is None:
                raise ValueError("No source DataFrame was provided")

            combined_df = self.fetch_foreign_keys(df=self.source_df, lookups=self.lookups)

            print(f"Transforming data from for {table} table...")
            transformed_df = self.transform(df=combined_df)

            final_df = transformed_df.dropDuplicates(subset=self.db_columns).dropna(how='any')    

            print(f"Loading {table} table data...")
            self.load(df=final_df, spark=self.spark, table=table)
            print(f"{table.title()} table data loaded successfully!")
        
        except Exception as e:
            print(f"[ERR]: An unexpected error occurred: {e}")
            raise

class SalesTLProcessor(BaseTLProcessor):
    def __init__(self, source_df: sp.DataFrame, db_columns: list[str], spark: sp.SparkSession, lookups: list[dict[str, str]]):
        super().__init__(source_df, db_columns, spark)

        self.lookups = lookups

    def process(self, table: str):
        try:
            if self.source_df is None:
                raise ValueError("No source DataFrame was provided")

            combined_df = self.fetch_foreign_keys(df=self.source_df, lookups=self.lookups)

            print(f"Transforming data from for {table} table...")
            transformed_df = self.transform(df=combined_df)

            final_df = transformed_df.dropDuplicates(subset=self.db_columns).dropna(how='any')    

            print(f"Loading {table} table data...")
            self.load(df=final_df, spark=self.spark, table=table)
            print(f"{table.title()} table data loaded successfully!")
        
        except Exception as e:
            print(f"[ERR]: An unexpected error occurred: {e}")
            raise
