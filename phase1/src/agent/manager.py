"""
Manager agents that handle high-level task coordination and system operations.

This module defines agents that act as managers or administrators, overseeing specific definition domains
like Todo lists or System files. They are responsible for understanding user commands
and dispatching them to the appropriate underlying skills.
"""
from src.agent.base import Agent, Skill
import src.agent.skills as skills

class TodoManager(Agent):
    """
    Agent responsible for managing the user's Todo list.
    
    This agent understands natural language commands related to task management
    (adding, listing, completing, etc.) and orchestrates the execution of these
    commands using the available task skills.
    """
    def __init__(self):
        super().__init__(
            name="TodoManager",
            persona=(
                "You are a dedicated and proactive productivity partner. Your goal isn't just to manage a list, "
                "but to help the user clear their mind and focus on what matters. You are organized, encouraging, "
                "and always ready to help clarify tasks or break them down into manageable steps."
            )
        )
        self._load_skills()

    def _load_skills(self):
        """
        Registers all task-related skills with the agent.
        
        This includes skills for:
        - creating and listing tasks
        - updating and completing tasks
        - searching and deleting tasks
        - getting statistics
        """
        self.add_skill(Skill.from_callable(skills.add_task))
        self.add_skill(Skill.from_callable(skills.list_tasks))
        self.add_skill(Skill.from_callable(skills.complete_task))
        self.add_skill(Skill.from_callable(skills.delete_task))
        self.add_skill(Skill.from_callable(skills.search_tasks))
        self.add_skill(Skill.from_callable(skills.update_task))
        self.add_skill(Skill.from_callable(skills.get_task_details))
        self.add_skill(Skill.from_callable(skills.get_statistics))

    def run(self, user_input: str) -> str:
        """
        Interprets user input and dispatches to the appropriate task skill.
        
        This method implements a command pattern matcher that:
        1. Parses the first word as the command/intent.
        2. Matches it against known aliases (e.g., "add", "new" -> add_task).
        3. Extracts arguments from the rest of the string.
        4. Invokes the corresponding skill.
        
        Args:
            user_input (str): The raw command string from the user.
            
        Returns:
            str: The result of the executed skill or an error message.
        """
        args = user_input.split()
        if not args:
            return "Please provide a command."

        command = args[0].lower()
        
        # Natural language aliases
        if command in ["add", "create", "new"]:
            title = " ".join(args[1:])
            if not title: return "Title required. Usage: add <task title>"
            return self.get_skill("add_task")(title=title)
            
        elif command in ["list", "show", "ls"]:
            status = "completed" if "completed" in args else ("pending" if "pending" in args else None)
            return self.get_skill("list_tasks")(status=status)
        
        elif command in ["search", "find"]:
            if len(args) < 2: return "Search query required. Usage: search <query>"
            query = " ".join(args[1:])
            return self.get_skill("search_tasks")(query=query)
            
        elif command in ["complete", "done", "finish"]:
            if len(args) < 2: return "Task ID required. Usage: complete <task-id>"
            return self.get_skill("complete_task")(task_id=args[1])
        
        elif command in ["update", "edit", "modify"]:
            if len(args) < 2: return "Task ID required. Usage: update <task-id> [field=value...]"
            return self.get_skill("update_task")(task_id=args[1])
            
        elif command in ["delete", "remove", "rm"]:
            if len(args) < 2: return "Task ID required. Usage: delete <task-id>"
            return self.get_skill("delete_task")(task_id=args[1])
        
        elif command in ["details", "info", "view"]:
            if len(args) < 2: return "Task ID required. Usage: details <task-id>"
            return self.get_skill("get_task_details")(task_id=args[1])
        
        elif command in ["stats", "statistics", "summary"]:
            return self.get_skill("get_statistics")()

        elif command in ["help", "?"]:
            return self.list_skills()
            
        else:
            return f"Unknown command '{command}'. Try 'help' to see available commands."

import src.agent.sys_skills as sys_skills

class SysAdminAgent(Agent):
    """
    Agent responsible for system administration and file operations.
    
    This agent provides a safe(r) interface for performing file system operations
    like reading, writing, and listing files, as well as running shell commands.
    """
    def __init__(self):
        super().__init__(
            name="SysAdmin",
            persona=(
                "You are a meticulous and reliable System Administrator. You treat the file system with the utmost care, "
                "always verifying paths and permissions before acting. You value precision and safety above all else, "
                "ensuring that every operation is safe and intended."
            )
        )
        self._load_skills()
        
    def _load_skills(self):
        """Loads filesystem and shell command skills."""
        self.add_skill(Skill.from_callable(sys_skills.read_file))
        self.add_skill(Skill.from_callable(sys_skills.write_file))
        self.add_skill(Skill.from_callable(sys_skills.list_directory))
        self.add_skill(Skill.from_callable(sys_skills.run_shell_command))
        self.add_skill(Skill.from_callable(sys_skills.grep_search))
        self.add_skill(Skill.from_callable(sys_skills.find_files))

    def run(self, user_input: str) -> str:
        """
        Parses and executes system administration commands.
        
        Supports commands for:
        - ls: List directory contents
        - read: Read file contents
        - write: Write to a file
        - run: Execute shell commands
        - find: Find files by pattern
        - grep: Search for text content
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
