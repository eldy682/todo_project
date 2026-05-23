import sqlite3

from app.errors.errors import DatabaseError

from .connection import get_conn


def execute_query(sql, params=(), fetch=False, return_lastrowid=False):
    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql, params)

        if fetch:
            rows = cursor.fetchall()
            return rows
        
        conn.commit()
        
        if return_lastrowid:
            return cursor.lastrowid
        
        return None
    
    except sqlite3.Error as e:
        conn.rollback()
        raise DatabaseError(f"数据库错误: {e}")
    
    finally:
        cursor.close()
        conn.close()