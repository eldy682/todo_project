from dotenv import load_dotenv
load_dotenv()

from db.init_db import init_db
from ui.app_menus import AppMenus
from service.task_service import TaskService
from service.ai_service import AIService
from repo.task_repo import TaskRepo
from db.base import execute_query


def main():
    init_db()

    repo = TaskRepo(execute_query)
    ai_service = AIService()
    service = TaskService(repo, ai_service)
    menus = AppMenus(service)

    menus.main_menu()

if __name__ == "__main__":
    main()