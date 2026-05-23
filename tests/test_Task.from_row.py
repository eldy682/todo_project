import pytest
from app.models.task import Task


def test_models_task_from_row():
    row = {
        "id": 1,
        "title": "Test Task",
        "status": "todo",
        "priority": 3,
        "category": "category",
        "tags": "tag1,tag2",
        "created_at": "2023-10-01",
        "due_at": "2023-10-02"
    }
    task = Task.from_row(row)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.status == "todo"
    assert task.priority == 3
    assert task.category == "category"
    assert task.tags == ["tag1", "tag2"]
    assert task.created_at == "2023-10-01"
    assert task.due_at == "2023-10-02"