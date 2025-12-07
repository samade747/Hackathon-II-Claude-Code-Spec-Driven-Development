from dataclasses import dataclass, field
from typing import Optional, Literal, List
import uuid
from src.todo.utils import now_iso # Import now_iso

@dataclass
class Task:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    status: Literal['pending', 'completed'] = 'pending'
    priority: Optional[Literal['high', 'medium', 'low']] = 'medium'
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso) # Use now_iso
    modified_at: Optional[str] = None
    due_date: Optional[str] = None
