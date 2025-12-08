from dataclasses import dataclass, field
from typing import Optional, Literal, List
import uuid
from src.todo.utils import now_iso # Import now_iso

@dataclass
class Task:
    """
    Represents a single todo item in the system.
    
    This dataclass serves as the core data model. It automatically generates
    unique IDs and creation timestamps for new tasks.
    
    Attributes:
        title (str): The main summary of the task.
        id (str): Unique UUID v4 identifier.
        description (Optional[str]): Detailed notes about the task.
        status (Literal['pending', 'completed']): Current state of execution.
        priority (Optional[Literal['high', 'medium', 'low']]): Urgency level.
        tags (List[str]): Arbitrary labels for categorization.
        created_at (str): ISO 8601 timestamp of creation.
        modified_at (Optional[str]): ISO 8601 timestamp of last update.
        due_date (Optional[str]): Optional deadline.
    """
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    status: Literal['pending', 'completed'] = 'pending'
    priority: Optional[Literal['high', 'medium', 'low']] = 'medium'
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso) # Use now_iso
    modified_at: Optional[str] = None
    due_date: Optional[str] = None

    def to_dict(self):
        """Converts the task to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "tags": self.tags,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "due_date": self.due_date,
        }
    
    def get_status_emoji(self) -> str:
        """Returns a checkmark '✓' for completed tasks, space for pending."""
        return "✓" if self.status == "completed" else " "
    
    def get_priority_color(self) -> str:
        """Returns a UI color string based on the task's priority."""
        if self.priority == "high":
            return "red"
        elif self.priority == "medium":
            return "yellow"
        elif self.priority == "low":
            return "green"
        return "white"

