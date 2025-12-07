import pytest
from unittest.mock import MagicMock, patch
from src.agent.manager import TodoManager

@pytest.fixture
def mock_storage():
    with patch('src.agent.skills._storage') as mock:
        yield mock

def test_manager_add_command(mock_storage):
    agent = TodoManager()
    mock_storage.add_task.return_value = None
    
    response = agent.run("add Buy Milk")
    
    assert "Task 'Buy Milk' added" in response
    mock_storage.add_task.assert_called_once()
    args, _ = mock_storage.add_task.call_args
    assert args[0].title == "Buy Milk"

def test_manager_list_command(mock_storage):
    agent = TodoManager()
    mock_storage.list_tasks.return_value = []
    
    response = agent.run("list")
    assert "No tasks found" in response
    mock_storage.list_tasks.assert_called_once()

def test_manager_list_filtered(mock_storage):
    agent = TodoManager()
    mock_storage.search_tasks.return_value = []
    
    response = agent.run("list pending")
    mock_storage.search_tasks.assert_called_with(status="pending", priority=None, tags=None)

def test_manager_help(mock_storage):
    agent = TodoManager()
    response = agent.run("help")
    assert "Available Skills:" in response
    assert "add_task" in response

def test_manager_unknown_command(mock_storage):
    agent = TodoManager()
    response = agent.run("dance")
    assert "Unknown command" in response
