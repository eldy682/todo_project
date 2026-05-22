from models.task import Task


class TaskRepo:
    def __init__(self, execute_query):
        self.execute_query = execute_query


    def get_task_by_id(self, task_id):
        where_sql = "WHERE tasks.id = ?"
        task = self._base_task_query(where_sql, (task_id,))
        return task

    def get_or_create_tag_id(self, tag):
        insert_sql = """
        INSERT OR IGNORE INTO tags(name) VALUES(?)
        """
        select_sql = """
        SELECT id FROM tags WHERE name = ?
        """

        self.execute_query(insert_sql, (tag,))
        rows = self.execute_query(select_sql, (tag,), fetch=True)
        return rows[0]["id"]


    def add_task(self, title, priority, due_at, category, tags):
        task_sql = """
        INSERT INTO tasks(title, status, priority, category, created_at, due_at)
                        VALUES(?, 'todo', ?, ?, datetime('now', '+8 hours'), ?)
        """
        task_tags_sql = """
        INSERT INTO task_tags(task_id, tag_id) VALUES(?, ?)
        """

        task_id = self.execute_query(task_sql, (title, priority, category, due_at), return_lastrowid=True)

        for tag in tags:
            tag_id = self.get_or_create_tag_id(tag)
            self.execute_query(task_tags_sql, (task_id, tag_id))



    def update_title(self, task_id, new_title):
        sql = """
        UPDATE tasks SET title = ? WHERE id = ?
        """
        self.execute_query(sql, (new_title, task_id))


    def update_due_at(self, task_id, new_due_at):
        sql = """
        UPDATE tasks SET due_at = ? WHERE id = ?
        """
        self.execute_query(sql, (new_due_at, task_id))


    def update_priority(self, task_id, new_priority):
        sql = """
        UPDATE tasks SET priority = ? WHERE id = ?
        """
        self.execute_query(sql, (new_priority, task_id))


    def done_task(self, task_id):
        sql = """
        UPDATE tasks SET status = 'done' WHERE id = ?
        """
        self.execute_query(sql, (task_id,))


    def undo_task(self, task_id):
        sql = """
        UPDATE tasks SET status = 'todo' WHERE id = ?
        """
        self.execute_query(sql, (task_id,))


    def delete_task(self, task_id):
        sql = """
        DELETE FROM tasks WHERE id = ?
        """
        self.execute_query(sql, (task_id,))


    def search_task(self, keyword):
        where_sql = "WHERE title LIKE ?"
        return self._base_task_query(where_sql, (f"%{keyword}%",))


    def list_tasks(self):
        return self._base_task_query()


    def list_overdue(self):
        where_sql = "WHERE due_at IS NOT NULL AND due_at < datetime('now', 'localtime') AND status = 'todo'"
        return self._base_task_query(where_sql)


    def list_today(self):
        where_sql = "WHERE due_at IS NOT NULL AND date(due_at) = date('now', 'localtime') AND status = 'todo'"
        return self._base_task_query(where_sql)

    def list_todo(self):
        where_sql = "WHERE status = 'todo'"
        return self._base_task_query(where_sql)


    def list_done(self):
        where_sql = "WHERE status = 'done'"
        return self._base_task_query(where_sql)


    def list_priority(self, min_p, max_p):
        where_sql = "WHERE priority BETWEEN ? AND ? AND status = 'todo'"
        return self._base_task_query(where_sql, (min_p, max_p))


    def list_all_categories(self):
        sql = """
        SELECT DISTINCT category FROM tasks
        """
        rows = self.execute_query(sql, fetch=True)
        return [row["category"] for row in rows if row["category"]]
    

    def list_all_tags(self):
        sql = """
        SELECT DISTINCT name FROM tags
        """
        rows = self.execute_query(sql, fetch=True)
        return [row["name"] for row in rows if row["name"]]
    

    def list_by_category(self, category):
        where_sql = "WHERE category = ? AND status = 'todo'"
        return self._base_task_query(where_sql, (category,))

    def list_by_tag(self, tag):
        where_sql = """
        WHERE tasks.id IN (
            SELECT task_id FROM task_tags
            JOIN tags ON task_tags.tag_id = tags.id
            WHERE tags.name = ?
        )
        """
        return self._base_task_query(where_sql, (tag,))


    def count_all_task(self):
        sql = """
        SELECT COUNT(*) as count FROM tasks
        """
        rows = self.execute_query(sql, fetch=True)
        return rows[0]["count"]


    def count_done_task(self):
        sql = """
        SELECT COUNT(*) as count FROM tasks WHERE status = 'done'
        """
        rows = self.execute_query(sql, fetch=True)
        return rows[0]["count"]

    def count_todo_task(self):
        sql = """
        SELECT COUNT(*) as count FROM tasks WHERE status = 'todo'
        """
        rows = self.execute_query(sql, fetch=True)
        return rows[0]["count"]
    
    def _base_task_query(self, where_sql="", params=()):
        sql = f"""
        SELECT tasks.*, GROUP_CONCAT(tags.name) AS tags FROM tasks
        LEFT JOIN task_tags ON tasks.id = task_tags.task_id
        LEFT JOIN tags ON task_tags.tag_id = tags.id
        {where_sql}
        GROUP BY tasks.id
        ORDER BY tasks.due_at
        """

        rows = self.execute_query(sql, params, fetch=True)
        return [Task.from_row(row) for row in rows]