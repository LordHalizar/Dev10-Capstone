import pyspark.sql as sp
from et_process import et_process
from tl_process_game import game_tl
from tl_process_game_genre import game_genre_tl
from tl_process_game_platform import game_platform_tl
from tl_process_game_platform_release import game_platform_release_tl
from tl_process_game_publisher import game_publisher_tl
from tl_process_genre import genre_tl
from tl_process_platform import platform_tl
from tl_process_publisher import publisher_tl
from tl_process_sales import sales_tl

spark = sp.SparkSession.builder.appName('ETLProcess').getOrCreate() 

source_df = et_process(spark=spark) 
genre_tl(source_df=source_df, db_columns=['genre_name'], spark=spark) 
publisher_tl(source_df=source_df, db_columns=['publisher_name'], spark=spark) 
game_tl(source_df=source_df, db_columns=['game_title'], spark=spark) 
platform_tl(source_df=source_df, db_columns=['platform_name'], spark=spark)
game_genre_tl(source_df=source_df, db_columns=['game_id', 'genre_id'], spark=spark)
game_publisher_tl(source_df=source_df, db_columns=['game_id', 'publisher_id'], spark=spark)
game_platform_tl(source_df=source_df, db_columns=['game_id', 'platform_id'], spark=spark)
game_platform_release_tl(source_df=source_df, db_columns=['game_platform_id', 'release_year'], spark=spark)
sales_tl(source_df=source_df, db_columns=['game_platform_release_id', 'na_sales', 'jp_sales'], spark=spark) 

spark.stop()