import pytest
from unittest.mock import MagicMock, patch
from src.todo.models import Task
import src.agent.skills as skills

@pytest.fixture
def mock_storage():
    with patch('src.agent.skills._storage') as mock:
        yield mock

def test_add_task_skill(mock_storage):
    mock_storage.add_task.return_value = None
    
    result = skills.add_task(title="Test Task", priority="high")
    assert "Task 'Test Task' added" in result
    mock_storage.add_task.assert_called_once()
    
    # Verify Task object creation
    args, _ = mock_storage.add_task.call_args
    assert isinstance(args[0], Task)
    assert args[0].title == "Test Task"
    assert args[0].priority == "high"

def test_list_tasks_skill(mock_storage):
    task1 = Task(title="Task 1", id="1")
    task2 = Task(title="Task 2", id="2")
    mock_storage.list_tasks.return_value = [task1, task2]
    
    result = skills.list_tasks()
    assert "Task 1" in result
    assert "Task 2" in result
    assert "ID: 1" in result
    
    mock_storage.list_tasks.assert_called_once()

def test_list_tasks_filtered(mock_storage):
    # If filters provided, search_tasks should be called
    mock_storage.search_tasks.return_value = []
    
    result = skills.list_tasks(status="pending")
    assert "No tasks found" in result
    mock_storage.search_tasks.assert_called_with(status="pending", priority=None, tags=None)

def test_complete_task_skill(mock_storage):
    result = skills.complete_task("task-id")
    assert "marked as completed" in result
    mock_storage.update_task.assert_called_with("task-id", status="completed")

def test_complete_task_not_found(mock_storage):
    mock_storage.update_task.side_effect = KeyError("Not found")
    result = skills.complete_task("task-id")
    assert "Error: Task with ID task-id not found" in result

def test_delete_task_skill(mock_storage):
    result = skills.delete_task("task-id")
    assert "deleted" in result
    mock_storage.delete_task.assert_called_with("task-id")
