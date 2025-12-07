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

import src.agent.sys_skills as sys_skills

class SysAdminAgent(Agent):
    def __init__(self):
        super().__init__(
            name="SysAdmin",
            persona="You are a system administrator responsible for file management and system operations."
        )
        self._load_skills()
        
    def _load_skills(self):
        self.add_skill(Skill.from_callable(sys_skills.read_file))
        self.add_skill(Skill.from_callable(sys_skills.write_file))
        self.add_skill(Skill.from_callable(sys_skills.list_directory))
        self.add_skill(Skill.from_callable(sys_skills.run_shell_command))
        self.add_skill(Skill.from_callable(sys_skills.grep_search))
        self.add_skill(Skill.from_callable(sys_skills.find_files))

    def run(self, user_input: str) -> str:
        """
        Simple dispatcher for SysAdmin.
        """
        args = user_input.split()
        if not args: return "Command required."
        cmd = args[0].lower()
        
        if cmd == "ls":
            path = args[1] if len(args) > 1 else "."
            return self.get_skill("list_directory")(path=path)
        elif cmd == "read":
            if len(args) < 2: return "File path required."
            return self.get_skill("read_file")(path=args[1])
        elif cmd == "write":
            if len(args) < 3: return "Path and content required."
            # naive parsing
            path = args[1]
            content = " ".join(args[2:])
            return self.get_skill("write_file")(path=path, content=content)
        elif cmd == "run":
            if len(args) < 2: return "Command required."
            shell_cmd = " ".join(args[1:])
            return self.get_skill("run_shell_command")(command=shell_cmd)
        elif cmd == "find":
            if len(args) < 2: return "Pattern required."
            return self.get_skill("find_files")(pattern=args[1])
        elif cmd == "grep":
            if len(args) < 2: return "Query required."
            return self.get_skill("grep_search")(query=args[1])
        elif cmd == "help":
            return self.list_skills()
        else:
            return "Unknown command. Try 'ls', 'read', 'write', 'run', 'find', 'grep', 'help'."
