import pytest
from unittest.mock import patch
from datetime import datetime, timezone # Ensure timezone is imported
import json
import io
import sys
import argparse

from src.todo.models import Task
from src.todo.utils import now_iso, parse_tags, validate_priority, validate_uuid
from src.todo.storage import InMemoryStorage
# Import functions directly for testing, not the main entry point
from src.todo.cli import storage, add_task, list_tasks_command, update_task_command, delete_task_command, complete_task_command 

# Mock datetime for deterministic tests
@pytest.fixture
def mock_datetime_utcnow(): 
    # Patch now_iso in both models (for Task creation) and storage (for modified_at)
    with patch('src.todo.models.now_iso') as mock_now_iso_models, \
         patch('src.todo.storage.now_iso') as mock_now_iso_storage:

        fixed_time = datetime(2025, 12, 7, 10, 0, 0, tzinfo=timezone.utc)
        fixed_time_iso = fixed_time.isoformat(timespec='seconds').replace('+00:00', 'Z')
        
        mock_now_iso_models.return_value = fixed_time_iso
        mock_now_iso_storage.return_value = fixed_time_iso
        
        yield

# --- Test Task Dataclass ---
def test_task_creation(mock_datetime_utcnow):
    task = Task(title="Test Task")
    assert task.title == "Test Task"
    assert task.status == "pending"
    assert task.priority == "medium"
    assert task.tags == []
    assert task.created_at == "2025-12-07T10:00:00Z"
    assert task.modified_at is None
    assert task.due_date is None
    assert isinstance(task.id, str)

def test_task_creation_with_all_fields(mock_datetime_utcnow):
    task = Task(
        title="Full Task",
        description="A full description",
        status="completed",
        priority="high",
        tags=["work", "urgent"],
        due_date="2025-12-08T12:00:00Z"
    )
    assert task.title == "Full Task"
    assert task.description == "A full description"
    assert task.status == "completed"
    assert task.priority == "high"
    assert task.tags == ["work", "urgent"]
    assert task.created_at == "2025-12-07T10:00:00Z"
    assert task.modified_at is None
    assert task.due_date == "2025-12-08T12:00:00Z"

# --- Test Utility Functions ---
def test_now_iso(mock_datetime_utcnow):
    assert now_iso() == "2025-12-07T10:00:00Z"

def test_parse_tags():
    assert parse_tags("tag1, tag2,tag3 ") == ["tag1", "tag2", "tag3"]
    assert parse_tags("") == []
    assert parse_tags("  ") == []
    assert parse_tags("single_tag") == ["single_tag"]

def test_validate_priority():
    validate_priority("high")
    validate_priority("medium")
    validate_priority("low")
    with pytest.raises(ValueError, match="Invalid priority: invalid. Must be 'high', 'medium', or 'low'."):
        validate_priority("invalid")

def test_validate_uuid():
    valid_uuid = "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    validate_uuid(valid_uuid)
    with pytest.raises(ValueError, match="Invalid UUID: invalid-uuid"):
        validate_uuid("invalid-uuid")

# --- Test InMemoryStorage ---
@pytest.fixture(autouse=True)
def clear_storage():
    """Clear storage before each test."""
    storage._tasks.clear()
    yield

def test_storage_add_task(mock_datetime_utcnow):
    task1 = Task(title="Task One")
    storage.add_task(task1)
    assert storage.get_task(task1.id) == task1
    assert len(storage.list_tasks()) == 1

def test_storage_add_task_empty_title_raises_error():
    with pytest.raises(ValueError, match="Task title cannot be empty."):
        task = Task(title="")
        storage.add_task(task)

def test_storage_delete_task(mock_datetime_utcnow):
    task1 = Task(title="Task One")
    storage.add_task(task1)
    storage.delete_task(task1.id)
    with pytest.raises(KeyError, match=f"Task with ID {task1.id} not found."):
        storage.get_task(task1.id)

def test_storage_delete_non_existent_task_raises_error():
    with pytest.raises(KeyError, match="Task with ID non-existent-id not found."):
        storage.delete_task("non-existent-id")

def test_storage_update_task(mock_datetime_utcnow):
    task1 = Task(title="Original Title", description="Original Desc")
    storage.add_task(task1)
    
    # Advance time for modified_at
    with patch('src.todo.storage.now_iso') as mock_now_iso_for_update:
        mock_now_iso_for_update.return_value = datetime(2025, 12, 7, 11, 0, 0, tzinfo=timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        updated_task = storage.update_task(task1.id, title="New Title", description="New Desc", priority="high")
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Desc"
        assert updated_task.priority == "high"
        assert updated_task.modified_at == "2025-12-07T11:00:00Z"

def test_storage_update_non_existent_task_raises_error():
    with pytest.raises(KeyError, match="Task with ID non-existent-id not found."):
        storage.update_task("non-existent-id", title="New Title")

def test_storage_list_tasks(mock_datetime_utcnow):
    task1 = Task(title="Task B", created_at="2025-12-07T09:00:00Z")
    task2 = Task(title="Task A", created_at="2025-12-07T10:00:00Z")
    storage.add_task(task1)
    storage.add_task(task2)
    tasks = storage.list_tasks()
    assert tasks == [task1, task2] # Should be sorted by created_at

def test_storage_get_task(mock_datetime_utcnow):
    task1 = Task(title="Task One")
    storage.add_task(task1)
    retrieved_task = storage.get_task(task1.id)
    assert retrieved_task == task1

def test_storage_get_non_existent_task_raises_error():
    with pytest.raises(KeyError, match="Task with ID non-existent-id not found."):
        storage.get_task("non-existent-id")

def test_storage_search_tasks(mock_datetime_utcnow):
    task1 = Task(title="Buy milk", description="2 liters", tags=["personal", "shopping"], status="pending", priority="high")
    task2 = Task(title="Finish report", description="Monthly work report", tags=["work"], status="pending", priority="medium")
    task3 = Task(title="Submit expense", tags=["work"], status="completed", priority="low")
    storage.add_task(task1)
    storage.add_task(task2)
    storage.add_task(task3)

    # Search by query
    results = storage.search_tasks(query="milk")
    assert results == [task1]

    results = storage.search_tasks(query="report")
    assert results == [task2]
    
    # query="work" should only find 'report' in description, not 'tags'
    results = storage.search_tasks(query="work")
    assert results == [task2]

    # Search by status
    results = storage.search_tasks(status="completed")
    assert results == [task3]

    # Search by priority
    results = storage.search_tasks(priority="high")
    assert results == [task1]

    # Search by tags
    results = storage.search_tasks(tags=["shopping"])
    assert results == [task1]

    results = storage.search_tasks(tags=["work"])
    assert sorted(results, key=lambda t: t.id) == sorted([task2, task3], key=lambda t: t.id)

    # Combined search
    results = storage.search_tasks(query="report", status="pending", priority="medium")
    assert results == [task2]

# --- Test CLI Commands ---
@pytest.fixture
def run_cli_command():
    """Helper to run a CLI command and capture stdout/stderr."""
    def _runner(command_func, args_list, capsys):
        # Create a mock args object
        MockArgs = type('MockArgs', (object,), {})
        args = MockArgs()
        
        # Dynamically populate args based on the expected arguments of the command_func
        # This is a simplification; a real parser would handle defaults, types, etc.
        # For direct function calls, we just need to ensure the args object has the right attributes.
        if command_func == add_task:
            args.title = args_list[1]
            args.description = None
            args.priority = 'medium'
            args.tags = ""
            args.due = None
            for i in range(len(args_list)):
                if args_list[i] == "--description": args.description = args_list[i+1]
                if args_list[i] == "--priority": args.priority = args_list[i+1]
                if args_list[i] == "--tags": args.tags = args_list[i+1]
                if args_list[i] == "--due": args.due = args_list[i+1]
        elif command_func == list_tasks_command:
            args.filter = None
            args.sort = None
            args.json = False
            for i in range(len(args_list)):
                if args_list[i] == "--filter": args.filter = args_list[i+1]
                if args_list[i] == "--sort": args.sort = args_list[i+1]
                if args_list[i] == "--json": args.json = True
        elif command_func == update_task_command:
            args.id = args_list[1]
            args.title = None
            args.description = None
            args.status = None
            args.priority = None
            args.tags = None
            args.due = None
            for i in range(len(args_list)):
                if args_list[i] == "--title": args.title = args_list[i+1]
                if args_list[i] == "--description": args.description = args_list[i+1]
                if args_list[i] == "--status": args.status = args_list[i+1]
                if args_list[i] == "--priority": args.priority = args_list[i+1]
                if args_list[i] == "--tags": args.tags = args_list[i+1]
                if args_list[i] == "--due": args.due = args_list[i+1]
        elif command_func == delete_task_command or command_func == complete_task_command:
            args.id = args_list[1]
        
        command_func(args)
        captured = capsys.readouterr()
        return captured.out, captured.err
    return _runner

def test_cli_add_task(run_cli_command, capsys, mock_datetime_utcnow):
    out, err = run_cli_command(add_task, ["add", "Buy milk", "--priority", "high", "--tags", "personal,shopping", "--due", "2025-12-10T09:00:00Z"], capsys)
    assert "Task 'Buy milk' added with ID:" in out
    assert not err
    
    tasks = storage.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"
    assert tasks[0].priority == "high"
    assert tasks[0].tags == ["personal", "shopping"]
    assert tasks[0].due_date == "2025-12-10T09:00:00Z"

def test_cli_add_task_invalid_priority(run_cli_command, capsys):
    out, err = run_cli_command(add_task, ["add", "Invalid Priority Task", "--priority", "super-high"], capsys)
    assert "Error adding task: Invalid priority: super-high" in err
    assert not out
    assert len(storage.list_tasks()) == 0

def test_cli_list_tasks(run_cli_command, capsys, mock_datetime_utcnow):
    # Add a task first
    task1 = Task(title="Task A")
    task2 = Task(title="Task B")
    storage.add_task(task1)
    storage.add_task(task2)

    out, err = run_cli_command(list_tasks_command, ["list"], capsys)
    assert "ID:" in out
    assert "Task A" in out
    assert "Task B" in out
    assert not err

def test_cli_list_tasks_json(run_cli_command, capsys, mock_datetime_utcnow):
    task1 = Task(title="JSON Task", status="pending")
    storage.add_task(task1)
    
    out, err = run_cli_command(list_tasks_command, ["list", "--json"], capsys)
    assert not err
    data = json.loads(out)
    assert len(data) == 1
    assert data[0]['title'] == "JSON Task"
    assert data[0]['status'] == "pending"

def test_cli_list_tasks_filter(run_cli_command, capsys, mock_datetime_utcnow):
    task1 = Task(title="Pending Task", status="pending")
    task2 = Task(title="Completed Task", status="completed")
    storage.add_task(task1)
    storage.add_task(task2)

    out, err = run_cli_command(list_tasks_command, ["list", "--filter", "status=completed"], capsys)
    assert "Completed Task" in out
    assert "Pending Task" not in out
    assert not err

def test_cli_list_tasks_sort(run_cli_command, capsys, mock_datetime_utcnow):
    task_high = Task(title="High Priority", priority="high", created_at="2025-12-07T10:00:00Z")
    task_medium = Task(title="Medium Priority", priority="medium", created_at="2025-12-07T10:00:01Z")
    task_low = Task(title="Low Priority", priority="low", created_at="2025-12-07T10:00:02Z")
    storage.add_task(task_low) # Add in arbitrary order
    storage.add_task(task_high)
    storage.add_task(task_medium)

    out, err = run_cli_command(list_tasks_command, ["list", "--sort", "created_at"], capsys)
    # Splitting by lines and checking order for more robustness
    output_lines = [line for line in out.splitlines() if "Title:" in line]
    assert "High Priority" in output_lines[0]
    assert "Medium Priority" in output_lines[1]
    assert "Low Priority" in output_lines[2]
    assert not err

def test_cli_update_task(run_cli_command, capsys, mock_datetime_utcnow):
    task = Task(title="Original", description="Original Desc")
    storage.add_task(task)
    
    # Advance time for modified_at
    with patch('src.todo.storage.now_iso') as mock_now_iso_for_update:
        mock_now_iso_for_update.return_value = datetime(2025, 12, 7, 11, 0, 0, tzinfo=timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        out, err = run_cli_command(update_task_command, ["update", task.id, "--title", "Updated Title", "--description", "Updated Desc"], capsys)
        assert f"Task '{task.id}' updated." in out
        assert not err

        updated_task = storage.get_task(task.id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Desc"
        assert updated_task.modified_at == "2025-12-07T11:00:00Z"

def test_cli_update_task_non_existent(run_cli_command, capsys):
    out, err = run_cli_command(update_task_command, ["update", "non-existent-id", "--title", "New Title"], capsys)
    assert "Error updating task: Invalid UUID: non-existent-id" in err
    assert not out

def test_cli_delete_task(run_cli_command, capsys, mock_datetime_utcnow):
    task = Task(title="To be deleted")
    storage.add_task(task)

    out, err = run_cli_command(delete_task_command, ["delete", task.id], capsys)
    assert f"Task '{task.id}' deleted." in out
    assert not err
    with pytest.raises(KeyError):
        storage.get_task(task.id)

def test_cli_delete_task_non_existent(run_cli_command, capsys):
    out, err = run_cli_command(delete_task_command, ["delete", "non-existent-id"], capsys)
    assert "Error deleting task: Invalid UUID: non-existent-id" in err
    assert not out

def test_cli_complete_task(run_cli_command, capsys, mock_datetime_utcnow):
    task = Task(title="To be completed")
    storage.add_task(task)
    
    # Advance time for modified_at
    with patch('src.todo.storage.now_iso') as mock_now_iso_for_update:
        mock_now_iso_for_update.return_value = datetime(2025, 12, 7, 12, 0, 0, tzinfo=timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        out, err = run_cli_command(complete_task_command, ["complete", task.id], capsys)
        assert f"Task '{task.id}' marked as completed." in out
        assert not err
        completed_task = storage.get_task(task.id)
        assert completed_task.status == "completed"
        assert completed_task.modified_at == "2025-12-07T12:00:00Z"

def test_cli_complete_task_non_existent(run_cli_command, capsys):
    out, err = run_cli_command(complete_task_command, ["complete", "non-existent-id"], capsys)
    assert "Error completing task: Invalid UUID: non-existent-id" in err
    assert not out
