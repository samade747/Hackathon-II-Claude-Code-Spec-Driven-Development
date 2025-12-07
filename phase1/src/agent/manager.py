from src.agent.base import Agent, Skill
import src.agent.skills as skills

class TodoManager(Agent):
    def __init__(self):
        super().__init__(
            name="TodoManager",
            persona="You are a helpful and efficient task manager. You allow users to manage their todo list."
        )
        self._load_skills()

    def _load_skills(self):
        """Loads available skills from the skills module."""
        self.add_skill(Skill.from_callable(skills.add_task))
        self.add_skill(Skill.from_callable(skills.list_tasks))
        self.add_skill(Skill.from_callable(skills.complete_task))
        self.add_skill(Skill.from_callable(skills.delete_task))

    def run(self, user_input: str) -> str:
        """
        Simple heuristic-based dispatcher for demonstration.
        In a real AI implementation, this would use an LLM to decide which tool to call 
        and extract parameters from `user_input`.
        """
        args = user_input.split()
        if not args:
            return "Please provide a command."

        command = args[0].lower()
        
        # Simple parser for demonstration
        if command == "add":
            # join the rest as title, very basic
            title = " ".join(args[1:])
            if not title: return "Title required."
            return self.get_skill("add_task")(title=title)
            
        elif command == "list":
            # check for simple filters
            status = "completed" if "completed" in args else ("pending" if "pending" in args else None)
            return self.get_skill("list_tasks")(status=status)
            
        elif command == "complete":
            if len(args) < 2: return "Task ID required."
            return self.get_skill("complete_task")(task_id=args[1])
            
        elif command == "delete":
            if len(args) < 2: return "Task ID required."
            return self.get_skill("delete_task")(task_id=args[1])

        elif command == "help":
            return self.list_skills()
            
        else:
            return f"I didn't understand that. Try 'help'. (Simulated Agent Logic)"
