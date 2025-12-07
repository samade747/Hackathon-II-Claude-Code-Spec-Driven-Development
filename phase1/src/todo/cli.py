import argparse
import json
from src.todo.models import Task
from src.todo.storage import InMemoryStorage
from src.todo.utils import parse_tags, validate_priority, validate_uuid, now_iso
import sys

# Initialize storage
storage = InMemoryStorage()

def add_task(args):
    try:
        if args.priority:
            validate_priority(args.priority)
        
        tags = parse_tags(args.tags) if args.tags else []

        task = Task(
            title=args.title,
            description=args.description,
            priority=args.priority,
            tags=tags,
            due_date=args.due
        )
        storage.add_task(task)
        print(f"Task '{task.title}' added with ID: {task.id}")
    except ValueError as e:
        print(f"Error adding task: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

def list_tasks_command(args):
    tasks = storage.list_tasks()

    # Filtering
    if args.filter:
        filter_key, filter_value = args.filter.split('=', 1)
        tasks = [task for task in tasks if getattr(task, filter_key, None) == filter_value]

    # Sorting
    if args.sort:
        tasks.sort(key=lambda task: getattr(task, args.sort, ''))

    if args.json:
        # Convert Task objects to dictionaries for JSON serialization
        tasks_dicts = []
        for task in tasks:
            task_dict = task.__dict__
            # Convert UUID to string if not already
            task_dict['id'] = str(task_dict['id'])
            tasks_dicts.append(task_dict)
        print(json.dumps(tasks_dicts, indent=2))
    else:
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            print(f"ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description or 'N/A'}")
            print(f"  Status: {task.status}")
            print(f"  Priority: {task.priority}")
            print(f"  Tags: {', '.join(task.tags) or 'N/A'}")
            print(f"  Created At: {task.created_at}")
            print(f"  Modified At: {task.modified_at or 'N/A'}")
            print(f"  Due Date: {task.due_date or 'N/A'}")
            print("-" * 20)

def update_task_command(args):
    try:
        validate_uuid(args.id)
        update_fields = {}
        if args.title:
            update_fields['title'] = args.title
        if args.description is not None:
            update_fields['description'] = args.description
        if args.status:
            update_fields['status'] = args.status
        if args.priority:
            validate_priority(args.priority)
            update_fields['priority'] = args.priority
        if args.tags is not None:
            update_fields['tags'] = parse_tags(args.tags)
        if args.due is not None:
            update_fields['due_date'] = args.due
        
        updated_task = storage.update_task(args.id, **update_fields)
        print(f"Task '{updated_task.id}' updated.")
    except (ValueError, KeyError) as e:
        print(f"Error updating task: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

def delete_task_command(args):
    try:
        validate_uuid(args.id)
        storage.delete_task(args.id)
        print(f"Task '{args.id}' deleted.")
    except (ValueError, KeyError) as e:
        print(f"Error deleting task: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

def complete_task_command(args):
    try:
        validate_uuid(args.id)
        updated_task = storage.update_task(args.id, status='completed')
        print(f"Task '{updated_task.id}' marked as completed.")
    except (ValueError, KeyError) as e:
        print(f"Error completing task: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="A simple console todo app.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo task")
    add_parser.add_argument("title", type=str, help="Title of the task")
    add_parser.add_argument("--description", type=str, help="Description of the task", default=None)
    add_parser.add_argument("--priority", type=str, choices=['high', 'medium', 'low'], help="Priority of the task", default='medium')
    add_parser.add_argument("--tags", type=str, help="Comma-separated tags for the task (e.g., work,personal)", default="")
    add_parser.add_argument("--due", type=str, help="Due date of the task (ISO 8601 format)", default=None)
    add_parser.set_defaults(func=add_task)

    # List command
    list_parser = subparsers.add_parser("list", help="List all todo tasks")
    list_parser.add_argument("--filter", type=str, help="Filter tasks by key=value (e.g., status=pending)", default=None)
    list_parser.add_argument("--sort", type=str, help="Sort tasks by a field (e.g., created_at, due_date)", default=None)
    list_parser.add_argument("--json", action="store_true", help="Output tasks in JSON format")
    list_parser.set_defaults(func=list_tasks_command)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing todo task")
    update_parser.add_argument("id", type=str, help="ID of the task to update")
    update_parser.add_argument("--title", type=str, help="New title of the task", default=None)
    update_parser.add_argument("--description", type=str, help="New description of the task", default=None)
    update_parser.add_argument("--status", type=str, choices=['pending', 'completed'], help="New status of the task", default=None)
    update_parser.add_argument("--priority", type=str, choices=['high', 'medium', 'low'], help="New priority of the task", default=None)
    update_parser.add_argument("--tags", type=str, help="Comma-separated tags for the task (e.g., work,personal)", default=None)
    update_parser.add_argument("--due", type=str, help="New due date of the task (ISO 8601 format)", default=None)
    update_parser.set_defaults(func=update_task_command)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo task")
    delete_parser.add_argument("id", type=str, help="ID of the task to delete")
    delete_parser.set_defaults(func=delete_task_command)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo task as completed")
    complete_parser.add_argument("id", type=str, help="ID of the task to mark as completed")
    complete_parser.set_defaults(func=complete_task_command)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
