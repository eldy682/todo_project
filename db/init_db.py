from .connection import get_conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'todo',
                priority INTEGER DEFAULT 2,
                created_at TEXT,
                due_at TEXT
                )
                """)
    conn.commit()
    conn.close()