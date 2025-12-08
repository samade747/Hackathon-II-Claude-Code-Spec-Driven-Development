from datetime import datetime, timezone
import uuid
from typing import List, Literal

def now_iso() -> str:
    """
    Returns the current UTC date and time in a standard ISO 8601 string format.
    
    Example: '2025-12-08T10:00:00Z'
    This format is used for consistent timestamp storage across the application.
    """
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def parse_tags(tags_str: str) -> List[str]:
    """
    Converts a comma-separated string of tags into a clean list of strings.
    
    Useful for parsing user input from the command line.
    Example: "work, urgent,  bug " -> ["work", "urgent", "bug"]
    
    Args:
        tags_str (str): A string containing tags separated by commas.
        
    Returns:
        List[str]: A list of cleaned tag strings.
    """
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]

def validate_priority(priority: str) -> None:
    """
    Ensures that a priority string is valid.
    
    Raises a ValueError if the priority is not one of: 'high', 'medium', 'low'.
    
    Args:
        priority (str): The value to check.
    """
    if priority not in ['high', 'medium', 'low']:
        raise ValueError(f"Invalid priority: {priority}. Must be 'high', 'medium', or 'low'.")

def validate_uuid(uuid_str: str) -> None:
    """
    Checks if a string is a valid UUID (Universally Unique Identifier).
    
    This is used to verify task IDs before attempting operations like update or delete.
    
    Args:
        uuid_str (str): The possible UUID string.
        
    Raises:
        ValueError: If the string is not a valid UUID.
    """
    try:
        uuid.UUID(uuid_str)
    except ValueError:
        raise ValueError(f"Invalid UUID: {uuid_str}")

