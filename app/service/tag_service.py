from app.service import service_helper
from app.repo.tag_repo import TagRepo


class TagService:
    def __init__(self, tag_repo: TagRepo):
        self.tag_repo = tag_repo

    def resolve_tags(self, tags):
        result = []

        tags = service_helper.normalize_tags(tags)
        for tag in tags:
            exist = self.tag_repo.get_tag_by_name(tag)

            if exist:
                result.append(exist["id"])
                continue

            new_id = self.tag_repo.get_or_create_tag_id(tag)
            result.append(new_id)
        
        return result