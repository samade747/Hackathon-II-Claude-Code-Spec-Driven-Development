from typing import List, Optional, Dict
from src.todo.models import Task
from src.todo.utils import now_iso, validate_priority
import json
from pathlib import Path
import os

class FileStorage:
    def __init__(self):
        self._storage_dir = Path.home() / ".todo_cli"
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._filepath = self._storage_dir / "tasks.json"
        self._tasks: Dict[str, Task] = {}
        self._load_tasks()

    def _load_tasks(self) -> None:
        if self._filepath.exists():
            try:
                with open(self._filepath, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                    for task_id, task_data in tasks_data.items():
                        self._tasks[task_id] = Task(**task_data)
            except json.JSONDecodeError:
                # Handle empty or corrupted JSON file
                self._tasks = {}
            except Exception as e:
                print(f"Error loading tasks: {e}")
                self._tasks = {}
        else:
            self._tasks = {}

    def _save_tasks(self) -> None:
        with open(self._filepath, 'w', encoding='utf-8') as f:
            json.dump({task_id: task.to_dict() for task_id, task in self._tasks.items()}, f, indent=4)

    def add_task(self, task: Task) -> None:
        if not task.title:
            raise ValueError("Task title cannot be empty.")
        if task.id in self._tasks:
            raise ValueError(f"Task with ID {task.id} already exists.")
        self._tasks[task.id] = task
        self._save_tasks()

    def delete_task(self, task_id: str) -> None:
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")
        del self._tasks[task_id]
        self._save_tasks()

    def update_task(self, task_id: str, **kwargs) -> Task:
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        task = self._tasks[task_id]
        updated = False
        for key, value in kwargs.items():
            if hasattr(task, key):
                if key == 'priority':
                    validate_priority(value)
                setattr(task, key, value)
                updated = True
        
        if updated:
            task.modified_at = now_iso()
        self._save_tasks()
        return task

    def list_tasks(self) -> List[Task]:
        # Sort by completion status (incomplete first), then by creation date
        return sorted(list(self._tasks.values()), key=lambda task: (task.status == 'completed', task.created_at))

    def get_task(self, task_id: str) -> Task:
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")
        return self._tasks[task_id]

    def search_tasks(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Task]:
        results = []
        for task in self._tasks.values():
            match = True
            if query:
                if query.lower() not in task.title.lower() and \
                   (task.description is None or query.lower() not in task.description.lower()):
                    match = False
            if status and task.status != status:
                match = False
            if priority and task.priority != priority:
                match = False
            if tags and not any(tag in task.tags for tag in tags):
                match = False
            
            if match:
                results.append(task)
        
        return sorted(results, key=lambda task: (task.status == 'completed', task.created_at))
