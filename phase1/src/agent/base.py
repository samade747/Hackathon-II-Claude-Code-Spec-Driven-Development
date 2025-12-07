from dataclasses import dataclass, field
from typing import Callable, List, Optional, Any, Dict
import inspect

@dataclass
class Skill:
    """Represents a capability that an agent can use."""
    name: str
    description: str
    func: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_callable(func: Callable, description: Optional[str] = None) -> 'Skill':
        """Creates a Skill from a python function, inspecting its signature."""
        sig = inspect.signature(func)
        params = {}
        for k, v in sig.parameters.items():
            if v.annotation != inspect.Parameter.empty:
                params[k] = getattr(v.annotation, "__name__", str(v.annotation))
            else:
                params[k] = "Any"
        
        doc = description or func.__doc__ or "No description provided."
        return Skill(
            name=func.__name__,
            description=doc.strip(),
            func=func,
            parameters=params
        )

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)

@dataclass
class Agent:
    """Base class for an agent."""
    name: str
    persona: str
    skills: List[Skill] = field(default_factory=list)

    def add_skill(self, skill: Skill) -> None:
        self.skills.append(skill)

    def get_skill(self, name: str) -> Optional[Skill]:
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def list_skills(self) -> str:
        """Returns a formatted list of available skills."""
        output = ["Available Skills:"]
        for skill in self.skills:
            params_str = ", ".join([f"{k}: {v}" for k, v in skill.parameters.items()])
            output.append(f"- {skill.name}({params_str}): {skill.description.splitlines()[0]}")
        return "\n".join(output)
        
    def run(self, user_input: str) -> str:
        """
        Placeholder for the 'thinking' loop. 
        In a real implementation, this would send the input + persona + skill definitions to an LLM.
        """
        raise NotImplementedError("Subclasses must implement run()")
