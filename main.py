from dotenv import load_dotenv
load_dotenv()

from app.db.init_db import init_db
from app.ui.app_menus import AppMenus
from app.service.task_service import TaskService
from app.ai.ai_service import AIService
from app.repo.task_repo import TaskRepo
from app.repo.tag_repo import TagRepo
from app.db.base import execute_query


def main():
    init_db()

    task_repo = TaskRepo(execute_query)
    tag_repo = TagRepo(execute_query)

    ai_service = AIService(tag_repo)
    service = TaskService(task_repo, tag_repo, ai_service)

    menus = AppMenus(service)

    menus.main_menu()

if __name__ == "__main__":
    main()