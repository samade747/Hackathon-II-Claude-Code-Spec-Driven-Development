from dataclasses import dataclass, field
from typing import Optional, Literal, List
import uuid
from datetime import datetime

@dataclass
class Task:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    status: Literal['pending', 'completed'] = 'pending'
    priority: Optional[Literal['high', 'medium', 'low']] = 'medium'
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec='seconds') + 'Z')
    modified_at: Optional[str] = None
    due_date: Optional[str] = None
