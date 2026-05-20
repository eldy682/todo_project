import sqlite3


DB_NAME = "todo.db"

def get_conn():
    return sqlite3.connect(DB_NAME)