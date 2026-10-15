SQL_FILE_PATH = "/opt/spark/files/in/sql/board_games_schema.sql"

def execute_board_game_schema():
    with open(SQL_FILE_PATH, 'r') as file:
        return file.read()