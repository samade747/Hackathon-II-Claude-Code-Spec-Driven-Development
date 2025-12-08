"""
System Administration Skills.

This module provides agents with capability to interact with the underlying operating system.
It includes skills for file manipulation (read/write), directory listing, and executing shell commands.
NOTE: These skills should be used with caution as they affect the real file system.
"""
import os
import subprocess
from glob import glob
from typing import List

def read_file(path: str) -> str:
    """
    Reads the entire content of a file as a string.
    
    Args:
        path: The absolute or relative path to the file.
        
    Returns:
        The content of the file or an error message if the file doesn't exist.
    """
    try:
        if not os.path.exists(path):
            return f"Error: File '{path}' does not exist."
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(path: str, content: str) -> str:
    """
    Writes text content to a file.
    
    WARNING: This will overwrite the file if it already exists.
    
    Args:
        path: Path to the file.
        content: The string content to write.
        
    Returns:
        Success or error message.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to '{path}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"

def list_directory(path: str = ".") -> str:
    """List contents of a directory."""
    try:
        entries = os.listdir(path)
        return "\n".join(entries) if entries else "Directory is empty."
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def run_shell_command(command: str) -> str:
    """
    Executes a shell command and returns the output.
    
    WARNING: High-risk capability. Use with extreme caution.
    This executes the command in a subprocess with a 10-second timeout.
    
    Args:
        command: The shell command string to execute.
        
    Returns:
        STDOUT and STDERR combined, or an error message.
    """
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR: {result.stderr}"
        return output
    except Exception as e:
        return f"Error running command: {str(e)}"

def grep_search(query: str, path: str = ".", recursive: bool = True) -> str:
    """
    Search for a text pattern in files (grep-like).
    
    Args:
        query: Pattern to search for.
        path: Directory to search in.
        recursive: Whether to search recursively.
    """
    try:
        # Use simpler grep command or python logic for cross-platform compatibility
        # Windows 'findstr' is roughly equivalent
        if os.name == 'nt':
            cmd = ['findstr', '/s', '/i', '/n', query, f"{path}\\*"] if recursive else ['findstr', '/i', '/n', query, f"{path}\\*"]
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return result.stdout if result.stdout else "No matches found."
        else:
            # Assume linux/mac grep
            cmd = ['grep', '-r', '-n', query, path] if recursive else ['grep', '-n', query, path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout if result.stdout else "No matches found."
    except Exception as e:
        return f"Error searching files: {str(e)}"

def find_files(pattern: str, path: str = ".") -> str:
    """
    Find files matching a glob pattern.
    
    Args:
        pattern: Glob pattern (e.g. "*.py").
        path: Root directory to start search.
    """
    try:
        search_path = os.path.join(path, "**", pattern)
        files = glob(search_path, recursive=True)
        return "\n".join(files) if files else "No files found."
    except Exception as e:
        return f"Error finding files: {str(e)}"
