from app.models.tag import Tag


class TagRepo:
    def __init__(self, execute_query):
        self.execute_query = execute_query

    
    def get_all_tags(self):
        sql = """
        SELECT * FROM tags
        """
        rows = self.execute_query(sql, fetch=True)
        return [Tag.from_row(row) for row in rows if row]
    

    def get_tag_by_name(self, name):
        sql = """
        SELECT * FROM tags WHERE name = ?
        """
        rows = self.execute_query(sql, (name,), fetch=True)
        return Tag.from_row(rows[0]) if rows else None
    

    def create_tag(self, name):
        sql = """
        INSERT OR IGNORE INTO tags(name) VALUES(?)
        """
        return self.execute_query(sql, (name,), return_lastrowid=True)

    
    def get_or_create_tag_id(self, name):
        self.create_tag(name)
        tag = self.get_tag_by_name(name)
        return tag.id if tag else None
        