from repo import task_repo as repo
from utils import datetime_helper
from service import service_helper


def add_task(title, priority, due_at):
    title = service_helper.normalize_title(title)
    priority = service_helper.normalize_priority(priority)
    due_at = datetime_helper.normalize_datetime(due_at)

    repo.add_task(title, priority, due_at)
    return "添加成功"


def update_title(task_id, new_title):
    service_helper.get_valid_task(task_id)
    new_title = service_helper.normalize_title(new_title)

    repo.update_title(task_id, new_title)
    return "更新任务标题成功"


def update_due_at(task_id, new_due_at):
    service_helper.get_valid_task(task_id)
    new_due_at = datetime_helper.normalize_datetime(new_due_at)
    
    repo.update_due_at(task_id, new_due_at)
    return "更新截止时间成功"


def update_priority(task_id, new_priority):
    service_helper.get_valid_task(task_id)
    new_priority = service_helper.normalize_priority(new_priority)

    repo.update_priority(task_id, new_priority)
    return "更新优先级成功"


def done_task(task_id):
    service_helper.get_valid_task(task_id)
    
    repo.done_task(task_id)
    return "完成任务成功"


def undo_task(task_id):
    service_helper.get_valid_task(task_id)
    
    repo.undo_task(task_id)
    return "撤销完成任务成功"


def delete_task(task_id):
    service_helper.get_valid_task(task_id)

    repo.delete_task(task_id)
    return "删除任务成功"


def search_task(keyword):
    keyword = service_helper.normalize_keyword(keyword)
    
    return repo.search_task(keyword)


def list_tasks():
    return repo.list_tasks()

def list_today():
    return repo.list_today()

def list_todo():
    return repo.list_todo()

def list_done():
    return repo.list_done()

def list_priority(min_p, max_p):
    return repo.list_priority(min_p, max_p)

def list_overdue():
    return repo.list_overdue()


def get_stats():
    return {
        "all": repo.count_all_task(),
        "done": repo.count_done_task(),
        "todo": repo.count_todo_task()
    }