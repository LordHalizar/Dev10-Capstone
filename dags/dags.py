import json
import logging
import os

import pandas as pd
import pendulum
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from dynaconf import Dynaconf
from sqlalchemy import create_engine

os.chdir(os.path.dirname(__file__))

SQL_FILE_PATH = "/opt/spark/files/in/sql/video_games_schema.sql"
SNOWFLAKE_FILE_PATH = "/opt/spark/files/in/sql/snowflake_schema.sql"

logger = logging.getLogger(__name__)

@dag(
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["postgres"],
)
def http_postgres_data_insert():
    def execute_video_games_schema():
        with open(SQL_FILE_PATH, 'r') as file:
            return file.read()
    sql_schema_task = SQLExecuteQueryOperator(
        task_id='execute_video_games_schema',
        conn_id='pg_conn',
        sql=execute_video_games_schema(),
        hook_params={
            "options": "-c search_path=video_games"
        }
    )
    
    data = {"app": "process_etl.py"}
    print(f"Submitting ETL job with data: {data}")
    logger.info(f"Submitting ETL job with data: {data}")
    http_etl_task = HttpOperator(
        task_id="http_etl_task",
        http_conn_id="http_spark",
        method="POST",
        headers={"Content-Type": "application/json"},
        endpoint="/submit",
        data=json.dumps(data),
    )
    logger.info("ETL job submitted successfully")

    sql_schema_task >> http_etl_task

@dag(
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["snowflake"],
)
def http_snowflake_data_insert():
    def execute_snowflake_schema():
        with open(SNOWFLAKE_FILE_PATH, 'r') as file:
            return file.read()

    snowflake_schema_task = SQLExecuteQueryOperator(
        task_id='execute_snowflake_task',
        conn_id='snowflake_conn',
        sql=execute_snowflake_schema(),
        hook_params={
            'account': 'NSBQTZA-ZK05168',
            'warehouse': 'COMPUTE_WH',
            'database': 'DEMO_DB',
            'schema': 'VIDEO_GAMES',
            'role': 'ACCOUNTADMIN',
        }
    )

    def copy_table_to_snowflake(table_name: str):
        settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
        engine = create_engine(settings.ENGINE_URL, echo=True)

        try:
            df = pd.read_sql(f'select * from "{table_name}"', engine)
        finally:
            engine.dispose()

        if df.empty:
            return 0

        hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
        conn = hook.get_conn()

        try:
            columns = list(df.columns)
            quoted_columns = ', '.join(f'"{column}"' for column in columns)
            placeholders = ', '.join(['%s'] * len(columns))
            insert_sql = (
                f'insert into "{table_name}" ({quoted_columns}) '
                f"values ({placeholders})"
            )

            rows = list(df.itertuples(index=False, name=None))

            with conn.cursor() as cursor:
                cursor.executemany(insert_sql, rows)

            conn.commit()
            return len(rows)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    copy_genre = PythonOperator(
        task_id='copy_genre',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'genre'}
    )
    copy_publisher = PythonOperator(
        task_id='copy_publisher',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'publisher'}
    )
    copy_game = PythonOperator(
        task_id='copy_game',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'game'}
    )
    copy_game_genre = PythonOperator(
        task_id='copy_game_genre',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'game_genre'}
    )
    copy_game_publisher = PythonOperator(
        task_id='copy_game_publisher',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'game_publisher'}
    )
    copy_platform = PythonOperator(
        task_id='copy_platform',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'platform'}
    )
    copy_game_platform = PythonOperator(
        task_id='copy_game_platform',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'game_platform'}
    )
    copy_game_platform_release = PythonOperator(
        task_id='copy_game_platform_release',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'game_platform_release'}
    )
    copy_sales = PythonOperator(
        task_id='copy_sales',
        python_callable=copy_table_to_snowflake,
        op_kwargs={'table_name': 'sales'}
    )

    snowflake_schema_task >> copy_genre >> copy_publisher >> copy_game >> copy_game_genre >> copy_game_publisher >> copy_platform >> copy_game_platform >> copy_game_platform_release >> copy_sales

http_postgres_data_insert()
http_snowflake_data_insert()
