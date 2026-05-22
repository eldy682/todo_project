from service import service_helper
from service.ai_service import AIService
from repo.task_repo import TaskRepo
from utils import datetime_helper
from utils.logger import logger


class TaskService:
    def __init__(self, repo: TaskRepo, ai_service: AIService):
        self.repo = repo
        self.ai_service = ai_service

    def add_task(self, title, priority, due_at):
        logger.info("add_task | title=%s | priority=%s | due_at=%s", title, priority, due_at)
        title = service_helper.normalize_title(title)
        priority = service_helper.normalize_priority(priority)
        due_at = datetime_helper.normalize_datetime(due_at)

        self.repo.add_task(title, priority, due_at)
        return "添加成功"
    

    def add_task_by_ai(self, text):
        logger.info("add_task_by_ai | text=%s", text)
        data = self.ai_service.parse_task(text)
        title = service_helper.normalize_title(data["title"])
        priority = service_helper.normalize_priority(data["priority"])
        due_at = datetime_helper.normalize_datetime(data["due_at"])
        category = service_helper.normalize_category(data["category"])
        tags = service_helper.normalize_tags(data["tags"])

        self.repo.add_task(title, priority, due_at, category, tags)
        return "添加成功"


    def update_title(self, task_id, new_title):
        logger.info("update_title | task_id=%s | new_title=%s", task_id, new_title)
        service_helper.get_valid_task(task_id)
        new_title = service_helper.normalize_title(new_title)

        self.repo.update_title(task_id, new_title)
        return "更新任务标题成功"


    def update_due_at(self, task_id, new_due_at):
        logger.info("update_due_at | task_id=%s | new_due_at=%s", task_id, new_due_at)
        service_helper.get_valid_task(task_id)
        new_due_at = datetime_helper.normalize_datetime(new_due_at)

        self.repo.update_due_at(task_id, new_due_at)
        return "更新截止时间成功"


    def update_priority(self, task_id, new_priority):
        logger.info("update_priority | task_id=%s | new_priority=%s", task_id, new_priority)
        service_helper.get_valid_task(task_id)
        new_priority = service_helper.normalize_priority(new_priority)

        self.repo.update_priority(task_id, new_priority)
        return "更新优先级成功"


    def done_task(self, task_id):
        logger.info("done_task | task_id=%s", task_id)
        service_helper.get_valid_task(task_id)

        self.repo.done_task(task_id)
        return "完成任务成功"


    def undo_task(self, task_id):
        logger.info("undo_task | task_id=%s", task_id)
        service_helper.get_valid_task(task_id)

        self.repo.undo_task(task_id)
        return "撤销完成任务成功"


    def delete_task(self, task_id):
        logger.info("delete_task | task_id=%s", task_id)
        service_helper.get_valid_task(task_id)

        self.repo.delete_task(task_id)
        return "删除任务成功"


    def search_task(self, keyword):
        logger.info("search_task | keyword=%s", keyword)
        keyword = service_helper.normalize_keyword(keyword)

        return self.repo.search_task(keyword)


    def list_tasks(self):
        logger.info("list_tasks")
        return self.repo.list_tasks()


    def list_today(self):
        logger.info("list_today")
        return self.repo.list_today()


    def list_todo(self):
        logger.info("list_todo")
        return self.repo.list_todo()


    def list_done(self):
        logger.info("list_done")
        return self.repo.list_done()


    def list_priority(self, min_p, max_p):
        logger.info("list_priority | min_p=%s | max_p=%s", min_p, max_p)
        return self.repo.list_priority(min_p, max_p)


    def list_overdue(self):
        logger.info("list_overdue")
        return self.repo.list_overdue()
    

    def list_all_categories(self):
        logger.info("list_all_categories")
        return self.repo.list_all_categories()
    
    
    def list_all_tags(self):
        logger.info("list_all_tags")
        return self.repo.list_all_tags()


    def list_by_category(self, category):
        logger.info("list_by_category | category=%s", category)
        category = service_helper.normalize_category(category)

        return self.repo.list_by_category(category)


    def list_by_tag(self, tag):
        logger.info("list_by_tag | tag=%s", tag)
        tag = service_helper.normalize_tag(tag)
        return self.repo.list_by_tag(tag)


    def get_stats(self):
        logger.info("get_stats")
        return {
            "all": self.repo.count_all_task(),
            "done": self.repo.count_done_task(),
            "todo": self.repo.count_todo_task()
        }