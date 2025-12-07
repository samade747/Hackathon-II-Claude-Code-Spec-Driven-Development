from typing import List, Optional
from src.todo.storage import FileStorage
from src.todo.models import Task
from src.todo.utils import now_iso

# Shared storage instance for skills
_storage = FileStorage()

def add_task(title: str, description: str = None, priority: str = "medium", tags: str = "") -> str:
    """
    Adds a new task to the list.
    
    Args:
        title: The title of the task.
        description: (Optional) Description of the task.
        priority: Priority level ('high', 'medium', 'low'). Default: 'medium'.
        tags: (Optional) Comma-separated tags (e.g., "work,urgent").
        
    Returns:
        A confirmation message with the Task ID.
    """
    tag_list = [t.strip() for t in tags.split(',')] if tags else []
    task = Task(
        title=title,
        description=description,
        priority=priority,
        tags=tag_list
    )
    _storage.add_task(task)
    return f"Task '{title}' added successfully. ID: {task.id}"

def list_tasks(status: str = None, priority: str = None, tag: str = None) -> str:
    """
    Lists tasks, optionally filtered.
    
    Args:
        status: (Optional) Filter by 'pending' or 'completed'.
        priority: (Optional) Filter by 'high', 'medium', 'low'.
        tag: (Optional) Filter by a specific tag.
        
    Returns:
        A formatted string list of tasks.
    """
    # map singular tag arg to list for storage search
    tags_filter = [tag] if tag else None
    
    # Use search_tasks for filtering if args provided, else list_tasks
    if status or priority or tags_filter:
        tasks = _storage.search_tasks(status=status, priority=priority, tags=tags_filter)
    else:
        tasks = _storage.list_tasks()

    if not tasks:
        return "No tasks found matching criteria."

    output = []
    for t in tasks:
        check = "[x]" if t.status == "completed" else "[ ]"
        prio = f"({t.priority})" if t.priority else ""
        tags_str = f"[{', '.join(t.tags)}]" if t.tags else ""
        output.append(f"{check} {t.title} {prio} {tags_str} - ID: {t.id}")
    
    return "\n".join(output)

def complete_task(task_id: str) -> str:
    """
    Marks a task as completed.
    
    Args:
        task_id: The UUID of the task to complete.
        
    Returns:
        Confirmation message.
    """
    try:
        _storage.update_task(task_id, status="completed")
        return f"Task {task_id} marked as completed."
    except KeyError:
        return f"Error: Task with ID {task_id} not found."

def delete_task(task_id: str) -> str:
    """
    Deletes a task.
    
    Args:
        task_id: The UUID of the task to delete.
        
    Returns:
        Confirmation message.
    """
    try:
        _storage.delete_task(task_id)
        return f"Task {task_id} deleted."
    except KeyError:
        return f"Error: Task with ID {task_id} not found."
