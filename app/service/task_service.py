from app.models.task import Task
from app.storage.file_storage import load_tasks, save_task


def add_task(description):
    tasks = load_tasks()
    task_id = max([task.id for task in tasks], default=0) + 1
    new_task = Task(id=task_id, description=description, completed=False)
    save_task(new_task)


def list_tasks():
    tasks = load_tasks()
    print(tasks)


def mark_task_completed(task_id):
    pass


def delete_task(task_id):
    pass