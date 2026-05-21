import os

from service import task_service as service
from service.errors import AppError
from utils.logger import logger


def handle_app_error(error):
    logger.warning(str(error))
    print(f"操作失败：{error}")
    pause()


def pause():
    input("\n按回车键继续...")


def show_tasks(tasks):
    if not tasks:
        print("暂无任务")
        pause()
        return
    print("\n" + "=" * 24 + "Tasks" + "=" * 25)
    print(f"{'ID':<5}{'TITLE':<15}{'STATUS':<10}{'P':<5}{'DUE_TIME':<15}")
    for task in tasks:
        print(f"{task[0]:<5}{task[1]:<15}{task[2]:<10}{task[3]:<5}{str(task[5]):<15}")
    pause()


def main_menu():
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
            add_task_menu()
        elif cmd == "2":
            tasks_menu()
        elif cmd == "3":
            update_task_menu()
        elif cmd == "4":
            done_task_menu()
        elif cmd == "5":
            delete_task_menu()
        elif cmd == "0":
            os.system("cls")
            break
        else:
            print("错误指令")
            pause()


def tasks_menu():
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
0. 返回
""")
        choice = input("选择: ")
        try:
            if choice == "1":
                show_tasks(service.list_tasks())
            elif choice == "2":
                show_tasks(service.list_today())
            elif choice == "3":
                show_tasks(service.list_todo())
            elif choice == "4":
                min_priority = input("最低优先级: ")
                max_priority = input("最高优先级: ")
                show_tasks(service.list_priority(min_priority, max_priority))
            elif choice == "5":
                show_tasks(service.list_overdue())
            elif choice == "6":
                show_stats()
            elif choice == "7":
                keyword = input("关键词: ")
                result = service.search_task(keyword)
                if result:
                    show_tasks(result)
                else:
                    print("未找到匹配任务")
                    pause()
            elif choice == "0":
                break
            else:
                print("错误指令")
                pause()
        except AppError as error:
            handle_app_error(error)
            

def add_task_menu():
    title = input("任务标题: ")
    priority = input("优先级(0~5): ")
    due_at = input("截止时间: ")

    try:
        message = service.add_task(title, priority, due_at)
        if message:
            print(message)
            pause()
    except AppError as error:
        handle_app_error(error)


def update_task_menu():
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
            message = service.update_title(task_id, new_title)
            if message:
                print(message)
                pause()

        elif choice == "2":
            new_due_at = input("更新时间: ")
            message = service.update_due_at(task_id, new_due_at)
            if message:
                print(message)
                pause()
            
        elif choice == "3":
            new_priority = input("更新优先级: ")
            message = service.update_priority(task_id, new_priority)
            if message:
                print(message)
                pause()

        else:
            print("错误指令")
            pause()
    except AppError as error:
        handle_app_error(error)


def done_task_menu():
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
            message = service.done_task(task_id)
            if message:
                print(message)
                pause()

        elif choice == "2":
            message = service.undo_task(task_id)
            if message:
                print(message)
                pause()

        else:
            print("错误指令")
            pause()
    except AppError as error:
        handle_app_error(error)


def delete_task_menu():
    task_id = input("任务id: ")
    try:
        message = service.delete_task(task_id)
        if message:
            print(message)
            pause()
    except AppError as error:
        handle_app_error(error)


def show_stats():
    stats = service.get_stats()
    print("======Stats======")
    print(f"总任务: {stats['all']}")
    print(f"已完成: {stats['done']}")
    print(f"未完成: {stats['todo']}")
    pause()