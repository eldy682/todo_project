

class Tag:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    
    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        
        return cls(
            id=row["id"],
            name=row["name"]
        )