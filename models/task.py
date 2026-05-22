

class Task:
    def __init__(self, id, title, status, priority, category, tags, created_at, due_at):
        self.id = id
        self.title = title
        self.status = status
        self.priority = priority
        self.category = category
        self.tags = tags
        self.created_at = created_at
        self.due_at = due_at


    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        
        tags = []
        if row["tags"]:
            tags = [tag.strip() for tag in row["tags"].split(",") if tag.strip()]

        return cls(
            id=row["id"],
            title=row["title"],
            status=row["status"],
            priority=row["priority"],
            category=row["category"],
            tags=tags,
            created_at=row["created_at"],
            due_at=row["due_at"]
        )