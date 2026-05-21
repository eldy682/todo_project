import os
import sqlite3


DB_NAME = "data/todo.db"

def get_conn():
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    return sqlite3.connect(DB_NAME)