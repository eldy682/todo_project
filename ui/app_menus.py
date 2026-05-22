import os
from wcwidth import wcswidth
from service.errors import AppError
from service.task_service import TaskService
from utils.logger import logger


class AppMenus:
    def __init__(self, task_service: TaskService):
        self.task_service = task_service

    
    def _pad(self, text, width):
        text = str(text)
        real_len = wcswidth(text)
        space = width - real_len
        return text + " " * max(space, 0)


    def handle_app_error(self, error, source):
        logger.error("操作失败 | source=%s | error=%s", source, str(error))
        print(f"操作失败：{error}")
        self.pause()


    def pause(self):
        input("\n按回车键继续...")


    def show_tasks(self, tasks):
        if not tasks:
            print("暂无任务")
            self.pause()
            return
        print("\n" + "=" * 40 + "Tasks" + "=" * 40)
        print(f"{'ID':<5}{'TITLE':<15}{'STATUS':<10}{'P':<5}{'CATEGORY':<15}{'TAGS':<15}{'DUE_TIME':<15}")
        for task in tasks:
            print(
                self._pad(task.id, 5) + 
                self._pad(task.title, 15) +
                self._pad(task.status, 10) +
                self._pad(task.priority, 5) +
                self._pad(task.category, 15) +
                self._pad(', '.join(task.tags), 15) +
                self._pad(str(task.due_at), 15)
            )
        self.pause()


    def main_menu(self):
        while True:
            os.system("cls")
            print("""
======TodoList======
1. 添加任务
2. 查看任务
3. 更新任务
4. 完成任务
5. 删除任务
0. 退出
""")

            cmd = input("选择: ")

            if cmd == "1":
                self.add_task_menu()
            elif cmd == "2":
                self.tasks_menu()
            elif cmd == "3":
                self.update_task_menu()
            elif cmd == "4":
                self.done_task_menu()
            elif cmd == "5":
                self.delete_task_menu()
            elif cmd == "0":
                os.system("cls")
                break
            else:
                print("错误指令")
                self.pause()


    def tasks_menu(self):
        while True:
            os.system("cls")
            print("""
======TodoList======
1. 全部任务
2. 今日任务
3. 代办任务
4. 优先任务
5. 过期任务
6. 统计数据
7. 搜索任务
8. 根据种类查看任务
9. 根据标签查看任务
0. 返回
""")
            choice = input("选择: ")
            try:
                if choice == "1":
                    self.show_tasks(self.task_service.list_tasks())
                elif choice == "2":
                    self.show_tasks(self.task_service.list_today())
                elif choice == "3":
                    self.show_tasks(self.task_service.list_todo())
                elif choice == "4":
                    min_priority = input("最低优先级: ")
                    max_priority = input("最高优先级: ")
                    self.show_tasks(self.task_service.list_priority(min_priority, max_priority))
                elif choice == "5":
                    self.show_tasks(self.task_service.list_overdue())
                elif choice == "6":
                    self.show_stats()
                elif choice == "7":
                    keyword = input("关键词: ")
                    result = self.task_service.search_task(keyword)
                    if result:
                        self.show_tasks(result)
                    else:
                        print("未找到匹配任务")
                        self.pause()
                elif choice == "8":
                    print("可用的任务种类:")
                    for category in self.task_service.list_all_categories():
                        print(f"- {category}")
                    category = input("任务种类: ")
                    self.show_tasks(self.task_service.list_by_category(category))
                elif choice == "9":
                    print("可用的标签:")
                    for tag in self.task_service.list_all_tags():
                        print(f"- {tag}")
                    tag = input("标签: ")
                    self.show_tasks(self.task_service.list_by_tag(tag))
                elif choice == "0":
                    break
                else:
                    print("错误指令")
                    self.pause()
            except AppError as error:
                self.handle_app_error(error, "查看任务")


    def add_task_menu(self):
        text = input("输入自然语言(按回车键跳过): ")
        if not text.strip():
            title = input("任务标题: ")
            priority = input("优先级(0~5): ")
            due_at = input("截止时间: ")

        try:
            if text.strip():
                message = self.task_service.add_task_by_ai(text)
            else:
                message = self.task_service.add_task(title, priority, due_at)
            if message:
                print(message)
                self.pause()
        except AppError as error:
            self.handle_app_error(error, "添加任务")


    def update_task_menu(self):
        os.system("cls")
        print("""
======Update======
1. 修改任务标题
2. 修改截止时间
3. 修改任务优先级
""")
        choice = input("选择: ")
        task_id = input("任务id: ")
        try:
            if choice == "1":
                new_title = input("更新标题: ")
                message = self.task_service.update_title(task_id, new_title)
                if message:
                    print(message)
                    self.pause()

            elif choice == "2":
                new_due_at = input("更新时间: ")
                message = self.task_service.update_due_at(task_id, new_due_at)
                if message:
                    print(message)
                    self.pause()
                
            elif choice == "3":
                new_priority = input("更新优先级: ")
                message = self.task_service.update_priority(task_id, new_priority)
                if message:
                    print(message)
                    self.pause()

            else:
                print("错误指令")
                self.pause()
        except AppError as error:
            self.handle_app_error(error, "更新任务")


    def done_task_menu(self):
        os.system("cls")
        print("""
======Done======
1. 完成任务
2. 撤销完成任务
0. 返回
""")
        choice = input("选择: ")
        task_id = input("任务id: ")
        try:
            if choice == "1":
                message = self.task_service.done_task(task_id)
                if message:
                    print(message)
                    self.pause()

            elif choice == "2":
                message = self.task_service.undo_task(task_id)
                if message:
                    print(message)
                    self.pause()

            else:
                print("错误指令")
                self.pause()
        except AppError as error:
            self.handle_app_error(error, "完成/撤销任务")


    def delete_task_menu(self):
        task_id = input("任务id: ")
        try:
            message = self.task_service.delete_task(task_id)
            if message:
                print(message)
                self.pause()
        except AppError as error:
            self.handle_app_error(error, "删除任务")


    def show_stats(self):
        stats = self.task_service.get_stats()
        print("======Stats======")
        print(f"总任务: {stats['all']}")
        print(f"已完成: {stats['done']}")
        print(f"未完成: {stats['todo']}")
        self.pause()