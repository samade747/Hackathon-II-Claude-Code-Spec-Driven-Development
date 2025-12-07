import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
import src.agent.sys_skills as sys_skills

def test_read_write_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    
    try:
        # Test Write
        res_write = sys_skills.write_file(path, "Hello World")
        assert "Successfully wrote" in res_write
        
        # Test Read
        res_read = sys_skills.read_file(path)
        assert res_read == "Hello World"
        
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_list_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a dummy file
        with open(os.path.join(tmpdir, "test.txt"), "w") as f:
            f.write("content")
            
        res = sys_skills.list_directory(tmpdir)
        assert "test.txt" in res

def test_run_shell_command():
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "Command Output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        res = sys_skills.run_shell_command("echo test")
        assert "Command Output" in res
        mock_run.assert_called_once()

def test_grep_search():
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "Found match at line 1"
        mock_run.return_value = mock_result
        
        # Test logic (mocked subprocess)
        res = sys_skills.grep_search("pattern", ".")
        assert "Found match" in res

def test_find_files():
    # Use real glob on a temp dir structure
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "subdir"))
        with open(os.path.join(tmpdir, "subdir", "found.py"), "w") as f: f.write("")
        with open(os.path.join(tmpdir, "ignored.txt"), "w") as f: f.write("")
        
        res = sys_skills.find_files("*.py", tmpdir)
        assert "found.py" in res
        assert "ignored.txt" not in res
