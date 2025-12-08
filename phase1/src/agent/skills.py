"""
Core Todo Skills for Agents.

This module exposes the functionality of the Todo application as "skills" that can be use by Agents.
These functions wrap the underlying `FileStorage` and logic into string-in/string-out (or simple primitive)
functions that are easy for an LLM or agent to invoke.
"""
from typing import List, Optional
from src.todo.storage import FileStorage
from src.todo.models import Task
from src.todo.utils import now_iso

# Shared storage instance for skills
# Agents using these skills will operate on the same persistent file storage.
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

def search_tasks(query: str) -> str:
    """
    Search tasks by query in title or description.
    
    Args:
        query: Search query string.
        
    Returns:
        Formatted list of matching tasks.
    """
    try:
        tasks = _storage.search_tasks(query=query)
        if not tasks:
            return f"No tasks found matching '{query}'."
        
        output = [f"Found {len(tasks)} task(s) matching '{query}':"]
        for t in tasks:
            check = "[x]" if t.status == "completed" else "[ ]"
            prio = f"({t.priority})" if t.priority else ""
            output.append(f"{check} {t.title} {prio} - ID: {t.id}")
        
        return "\n".join(output)
    except Exception as e:
        return f"Error searching tasks: {e}"

def update_task(task_id: str, title: str = None, description: str = None, 
                priority: str = None, status: str = None) -> str:
    """
    Update a task's fields.
    
    Args:
        task_id: The UUID of the task to update.
        title: (Optional) New title.
        description: (Optional) New description.
        priority: (Optional) New priority ('high', 'medium', 'low').
        status: (Optional) New status ('pending', 'completed').
        
    Returns:
        Confirmation message.
    """
    try:
        update_fields = {}
        if title: update_fields['title'] = title
        if description is not None: update_fields['description'] = description
        if priority: update_fields['priority'] = priority
        if status: update_fields['status'] = status
        
        if not update_fields:
            return "No fields specified for update."
        
        _storage.update_task(task_id, **update_fields)
        return f"Task {task_id} updated successfully."
    except KeyError:
        return f"Error: Task with ID {task_id} not found."
    except Exception as e:
        return f"Error updating task: {e}"

def get_task_details(task_id: str) -> str:
    """
    Get detailed information about a specific task.
    
    Args:
        task_id: The UUID of the task.
        
    Returns:
        Detailed task information.
    """
    try:
        task = _storage.get_task(task_id)
        output = [
            f"Task Details:",
            f"  ID: {task.id}",
            f"  Title: {task.title}",
            f"  Description: {task.description or 'N/A'}",
            f"  Status: {task.status}",
            f"  Priority: {task.priority}",
            f"  Tags: {', '.join(task.tags) if task.tags else 'N/A'}",
            f"  Created: {task.created_at}",
            f"  Modified: {task.modified_at or 'Never'}",
            f"  Due Date: {task.due_date or 'No due date'}"
        ]
        return "\n".join(output)
    except KeyError:
        return f"Error: Task with ID {task_id} not found."

def get_statistics() -> str:
    """
    Get statistics about all tasks.
    
    Returns:
        Task statistics summary.
    """
    tasks = _storage.list_tasks()
    total = len(tasks)
    completed = len([t for t in tasks if t.status == "completed"])
    pending = total - completed
    high_priority = len([t for t in tasks if t.priority == "high" and t.status == "pending"])
    
    output = [
        "Task Statistics:",
        f"  Total tasks: {total}",
        f"  Completed: {completed}",
        f"  Pending: {pending}",
        f"  High priority (pending): {high_priority}"
    ]
    return "\n".join(output)
