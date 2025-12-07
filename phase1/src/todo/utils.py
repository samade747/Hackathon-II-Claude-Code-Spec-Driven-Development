from datetime import datetime
import uuid
from typing import List, Literal

def now_iso() -> str:
    """Returns the current UTC time in ISO 8601 format."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'

def parse_tags(tags_str: str) -> List[str]:
    """Parses a comma-separated string of tags into a list of stripped tag strings."""
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]

def validate_priority(priority: str) -> None:
    """Raises a ValueError if the priority is not 'high', 'medium', or 'low'."""
    if priority not in ['high', 'medium', 'low']:
        raise ValueError(f"Invalid priority: {priority}. Must be 'high', 'medium', or 'low'.")

def validate_uuid(uuid_str: str) -> None:
    """Raises a ValueError if the string is not a valid UUID."""
    try:
        uuid.UUID(uuid_str)
    except ValueError:
        raise ValueError(f"Invalid UUID: {uuid_str}")

