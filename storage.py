import json
import os
from typing import List, Optional
from models import Task

DATA_FILE = "tasks.json"


def _load_raw() -> List[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_raw(data: List[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_all() -> List[Task]:
    return [Task.from_dict(d) for d in _load_raw()]


def save_all(tasks: List[Task]) -> None:
    _save_raw([t.to_dict() for t in tasks])


def find_by_id(task_id: str) -> Optional[Task]:
    for task in load_all():
        if task.id == task_id:
            return task
    return None


def add(task: Task) -> None:
    tasks = load_all()
    tasks.append(task)
    save_all(tasks)


def update(task: Task) -> bool:
    tasks = load_all()
    for i, t in enumerate(tasks):
        if t.id == task.id:
            tasks[i] = task
            save_all(tasks)
            return True
    return False


def delete(task_id: str) -> bool:
    tasks = load_all()
    filtered = [t for t in tasks if t.id != task_id]
    if len(filtered) == len(tasks):
        return False
    save_all(filtered)
    return True
