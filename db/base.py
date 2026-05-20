from .connection import get_conn


def execute_query(sql, params=(), fetch=False):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(sql, params)

    if fetch:
        result = cursor.fetchall()
    else:
        result = None

    conn.commit()
    conn.close()

    return result