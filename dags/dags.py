import logging
import os

import json

import pendulum
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import dag, task

os.chdir(os.path.dirname(__file__))

SQL_FILE_PATH = "/opt/spark/files/in/sql/video_games_schema.sql"

logger = logging.getLogger(__name__)

@dag(
    # schedule='*/3 * * * *',
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
http_postgres_data_insert()