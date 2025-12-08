from dataclasses import dataclass, field
from typing import Callable, List, Optional, Any, Dict
import inspect

@dataclass
class Skill:
    """
    Represents a specific capability or tool that an agent can use.
    
    Skills are the fundamental building blocks of an agent's abilities. They wrap
    Python functions (callables) and provide metadata like name, description,
    and parameter definitions that are useful for agents to understand and use them.

    Attributes:
        name (str): The name of the skill, typically the function name.
        description (str): A natural language description of what the skill does.
        func (Callable): The actual python function to execute.
        parameters (Dict[str, Any]): A dictionary describing the expected parameters.
    """
    name: str
    description: str
    func: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_callable(func: Callable, description: Optional[str] = None) -> 'Skill':
        """
        Creates a Skill instance from a python function by inspecting its signature.
        
        This method uses the `inspect` module to automatically derive parameter names
        and types from the function's type hints. This makes it easy to turn standard
        Python functions into agent skills.

        Args:
            func (Callable): The function to convert into a skill.
            description (Optional[str]): An optional description override. If not provided,
                                         the function's docstring will be used.

        Returns:
            Skill: The initialized Skill object.
        """
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
        """Executes the wrapped function."""
        return self.func(*args, **kwargs)

@dataclass
class Agent:
    """
    Base class for an autonomous agent.
    
    An Agent has a persona (identity) and a collection of Skills (capabilities).
    It is designed to interact with a user, understand their intent, and select
    the appropriate tools (skills) to fulfill requests.

    Attributes:
        name (str): The name of the agent.
        persona (str): The system prompt or personality definition of the agent.
        skills (List[Skill]): A list of skills currently available to the agent.
    """
    name: str
    persona: str
    skills: List[Skill] = field(default_factory=list)

    def add_skill(self, skill: Skill) -> None:
        """Adds a new skill to the agent's repertoire."""
        self.skills.append(skill)

    def get_skill(self, name: str) -> Optional[Skill]:
        """
        Retrieves a skill by its name.
        
        Args:
            name (str): The name of the skill to retrieve.
            
        Returns:
            Optional[Skill]: The matching Skill object or None if not found.
        """
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def list_skills(self) -> str:
        """
        Returns a human-readable formatted list of available skills and their signatures.
        
        Returns:
            str: A formatted string listing all skills.
        """
        output = ["Available Skills:"]
        for skill in self.skills:
            params_str = ", ".join([f"{k}: {v}" for k, v in skill.parameters.items()])
            output.append(f"- {skill.name}({params_str}): {skill.description.splitlines()[0]}")
        return "\n".join(output)
        
    def run(self, user_input: str) -> str:
        """
        The main execution entry point for the agent.
        
        This method processes user input and returns a response.
        Subclasses must implement the specific logic for interpreting input
        and choosing skills.

        Args:
            user_input (str): The text input from the user.

        Returns:
            str: The agent's response.
        """
        raise NotImplementedError("Subclasses must implement run()")
