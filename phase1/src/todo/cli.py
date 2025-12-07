import argparse
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from src.todo.models import Task
from src.todo.storage import FileStorage, InMemoryStorage
from src.todo.utils import parse_tags, validate_priority, validate_uuid, now_iso

# Initialize Rich console
console = Console()

# Global storage (defaults to FileStorage for backwards compatibility)
storage = FileStorage()

def get_storage(storage_type='file'):
    """Get storage instance based on type."""
    if storage_type == 'memory':
        return InMemoryStorage()
    else:
        return FileStorage()

def format_task_rich(task: Task) -> Panel:
    """Format a single task as a rich panel."""
    emoji = task.get_status_emoji()
    priority_color = task.get_priority_color()
    
    content = f"""[bold]{task.title}[/bold]
[dim]ID: {task.id}[/dim]
Status: [{emoji}] {task.status}
Priority: [{priority_color}]{task.priority}[/{priority_color}]
Tags: {', '.join(task.tags) if task.tags else 'None'}
Created: {task.created_at}
Modified: {task.modified_at or 'Never'}
Due: {task.due_date or 'No due date'}"""
    
    if task.description:
        content += f"\n\n{task.description}"
    
    border_style = "green" if task.status == "completed" else priority_color
    return Panel(content, border_style=border_style)

def format_tasks_table(tasks: list[Task]) -> Table:
    """Format tasks as a rich table."""
    table = Table(title="📋 Tasks", show_header=True, header_style="bold cyan")
    table.add_column("✓", style="green", width=3)
    table.add_column("Title", style="white")
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Tags", style="dim")
    table.add_column("Due Date", style="yellow", width=12)
    table.add_column("ID", style="dim", width=8)
    
    for task in tasks:
        emoji = task.get_status_emoji()
        priority_color = task.get_priority_color()
        priority_text = f"[{priority_color}]{task.priority}[/{priority_color}]"
        tags_text = ', '.join(task.tags[:2]) if task.tags else ""
        due_text = task.due_date[:10] if task.due_date else ""
        short_id = task.id[:8]
        
        # Strikethrough for completed tasks
        title = f"[dim]{task.title}[/dim]" if task.status == "completed" else task.title
        
        table.add_row(emoji, title, priority_text, tags_text, due_text, short_id)
    
    return table

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
        
        if args.format == 'rich':
            console.print(f"[bold green]✓ Task '{task.title}' added successfully![/bold green]", style="green")
            console.print(f"[dim]ID: {task.id}[/dim]")
        else:
            print(f"Task '{task.title}' added with ID: {task.id}")
    except ValueError as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Error:[/bold red] {e}", style="red")
        else:
            print(f"Error adding task: {e}", file=sys.stderr)
    except Exception as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Unexpected error:[/bold red] {e}", style="red")
        else:
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

    if args.format == 'json':
        # JSON output
        tasks_dicts = [task.to_dict() for task in tasks]
        print(json.dumps(tasks_dicts, indent=2))
    elif args.format == 'rich':
        # Rich table output
        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return
        table = format_tasks_table(tasks)
        console.print(table)
    else:
        # Plain text output
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
        
        if args.format == 'rich':
            console.print(f"[bold green]✓ Task updated successfully![/bold green]")
        else:
            print(f"Task '{updated_task.id}' updated.")
    except (ValueError, KeyError) as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Error:[/bold red] {e}", style="red")
        else:
            print(f"Error updating task: {e}", file=sys.stderr)
    except Exception as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Unexpected error:[/bold red] {e}", style="red")
        else:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

def delete_task_command(args):
    try:
        validate_uuid(args.id)
        storage.delete_task(args.id)
        
        if args.format == 'rich':
            console.print(f"[bold green]✓ Task deleted successfully![/bold green]")
        else:
            print(f"Task '{args.id}' deleted.")
    except (ValueError, KeyError) as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Error:[/bold red] {e}", style="red")
        else:
            print(f"Error deleting task: {e}", file=sys.stderr)
    except Exception as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Unexpected error:[/bold red] {e}", style="red")
        else:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

def complete_task_command(args):
    try:
        validate_uuid(args.id)
        updated_task = storage.update_task(args.id, status='completed')
        
        if args.format == 'rich':
            console.print(f"[bold green]✓ Task marked as completed![/bold green]")
            console.print(f"[dim]{updated_task.title}[/dim]")
        else:
            print(f"Task '{updated_task.id}' marked as completed.")
    except (ValueError, KeyError) as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Error:[/bold red] {e}", style="red")
        else:
            print(f"Error completing task: {e}", file=sys.stderr)
    except Exception as e:
        if args.format == 'rich':
            console.print(f"[bold red]✗ Unexpected error:[/bold red] {e}", style="red")
        else:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="A simple console todo app with rich formatting.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global arguments
    parser.add_argument(
        '--storage',
        type=str,
        choices=['memory', 'file'],
        default='file',
        help='Storage backend: memory (in-memory, not persisted) or file (JSON file, persisted)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['plain', 'rich', 'json'],
        default='rich',
        help='Output format: plain, rich (with colors and tables), or json'
    )
    
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

    # Override storage if user explicitly specifies it
    if args.storage:
        global storage
        storage = get_storage(args.storage)

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
