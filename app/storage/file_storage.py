import os
import json
from app.models.task import Task

FILE_PATH = os.path.join("data", "tasks.json")


def load_tasks():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
        # return data
        return [Task.from_dict(task) for task in data]


def save_task(task):
    tasks = load_tasks()
    tasks.append(task)
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump([t.to_dict() for t in tasks], file, ensure_ascii=False, indent=4)
    print(f"Task {task.id} saved to file.")