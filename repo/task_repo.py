from db.base import execute_query
import sqlite3

DB_NAME = "todo.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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


def get_task_by_id(task_id):
    sql = "SELECT * FROM tasks WHERE id = ?"
    return execute_query(sql, (task_id,), fetch=True) 


def add_task(title, priority, due_at):
    sql = """
INSERT INTO tasks(title, status, priority, created_at, due_at)
                VALUES(?, 'todo', ?, datetime('now', '+8 hours'), ?)
"""
    execute_query(sql, (title, priority, due_at))



def update_title(task_id, new_title):
    sql = """
UPDATE tasks SET title = ? WHERE id = ?
"""
    execute_query(sql, (new_title, task_id))


def update_due_at(task_id, new_due_at):
    sql = """
UPDATE tasks SET due_at = ? WHERE id = ?
"""
    execute_query(sql, (new_due_at, task_id))


def update_priority(task_id, new_priority):
    sql = """
UPDATE tasks SET priority = ? WHERE id = ?
"""
    execute_query(sql, (new_priority, task_id))


def done_task(task_id):
    sql = """
UPDATE tasks SET status = 'done' WHERE id = ?
"""
    execute_query(sql, (task_id,))


def undo_task(task_id):
    sql = """
UPDATE tasks SET status = 'todo' WHERE id = ?
"""
    execute_query(sql, (task_id,))


def delete_task(task_id):
    sql = """
DELETE FROM tasks WHERE id = ?
"""
    execute_query(sql, (task_id,))


def search_task(keyword):
    sql = """
SELECT * FROM tasks WHERE title like ? ORDER BY due_at
"""
    return execute_query(sql, (f"%{keyword}%",), fetch=True)


def list_tasks():
    sql = """
SELECT * FROM tasks ORDER BY due_at
"""
    return execute_query(sql, fetch=True)


def list_overdue():
    sql = """
SELECT * FROM tasks WHERE due_at IS NOT NULL AND due_at < datetime('now', '+8 hours') AND status != 'done' ORDER BY due_at
"""
    return execute_query(sql, fetch=True)


def list_today():
    sql = """
SELECT * FROM tasks WHERE due_at IS NOT NULL AND date(due_at) = date('now', 'localtime') ORDER BY due_at
"""
    return execute_query(sql, fetch=True)


def list_todo():
    sql = """
SELECT * FROM tasks WHERE status = 'todo' ORDER BY due_at
"""
    return execute_query(sql, fetch=True)


def list_done():
    sql = """
SELECT * FROM tasks WHERE status = 'done' ORDER BY due_at
"""
    return execute_query(sql, fetch=True)


def list_priority(min_p, max_p):
    sql = """
SELECT * FROM tasks WHERE priority >= ? AND priority <= ? ORDER BY priority DESC
"""
    return execute_query(sql, (min_p, max_p), fetch=True)


def count_all_task():
    sql = """
SELECT COUNT(*) FROM tasks
"""
    result = execute_query(sql, fetch=True)
    return result[0][0]


def count_done_task():
    sql = """
SELECT COUNT(*) FROM tasks WHERE status = 'done'
"""
    result = execute_query(sql, fetch=True)
    return result[0][0]

def count_todo_task():
    sql = """
SELECT COUNT(*) FROM tasks WHERE status = 'todo'
"""
    result = execute_query(sql, fetch=True)
    return result[0][0]