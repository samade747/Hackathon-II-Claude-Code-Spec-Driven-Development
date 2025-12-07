import os
import sys
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from src.agent.manager import TodoManager, SysAdminAgent

# Initialize Console
console = Console()

class TUI:
    def __init__(self):
        self.todo_agent = TodoManager()
        self.sys_agent = SysAdminAgent()
        self.current_agent = self.todo_agent
        self.chat_history = []
        self.running = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_header(self) -> Panel:
        title = f"🤖 Claude Code - Evolution of Todo (Phase IV)"
        subtitle = f"Active Agent: {self.current_agent.name} | Type 'switch <agent>' to change | 'exit' to quit"
        return Panel(Text(subtitle, justify="center"), title=title, style="bold cyan")

    def render_chat(self) -> Panel:
        # Show last 10 messages
        messages = self.chat_history[-10:]
        text = "\n".join(messages) if messages else "Start chatting..."
        return Panel(text, title="💬 Chat History", style="white")

    def render_tasks(self) -> Panel:
        # Use TodoManager logic to get tasks for display
        # We invoke list_tasks skill directly for visualization
        try:
            tasks_str = self.todo_agent.get_skill("list_tasks")()
        except:
            tasks_str = "Error loading tasks."
        return Panel(tasks_str, title="📋 Current Tasks", style="green")

    def render(self):
        self.clear_screen()
        
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        layout["main"].split_row(
            Layout(name="chat", ratio=2),
            Layout(name="tasks", ratio=1)
        )

        layout["header"].update(self.render_header())
        layout["chat"].update(self.render_chat())
        layout["tasks"].update(self.render_tasks())
        layout["footer"].update(Panel("Type your command below...", style="grey50"))

        console.print(layout)

    def process_input(self, user_input: str):
        self.chat_history.append(f"[yellow]User:[/yellow] {user_input}")
        
        args = user_input.strip().split()
        if not args: return

        cmd = args[0].lower()

        if cmd in ["exit", "quit"]:
            self.running = False
            return

        elif cmd == "switch":
            if len(args) < 2:
                response = "Available agents: todo, sysadmin"
            else:
                target = args[1].lower()
                if target == "todo":
                    self.current_agent = self.todo_agent
                    response = "Switched to TodoManager."
                elif target == "sysadmin":
                    self.current_agent = self.sys_agent
                    response = "Switched to SysAdmin."
                else:
                    response = f"Unknown agent '{target}'. Available: todo, sysadmin"
            self.chat_history.append(f"[blue]System:[/blue] {response}")
            return

        elif cmd == "clear":
            self.chat_history = []
            return

        # Pass to current agent
        response = self.current_agent.run(user_input)
        self.chat_history.append(f"[green]{self.current_agent.name}:[/green] {response}")

    def loop(self):
        while self.running:
            self.render()
            try:
                user_input = console.input("\n[bold cyan]>>> [/bold cyan]")
                if user_input:
                    self.process_input(user_input)
            except KeyboardInterrupt:
                self.running = False

if __name__ == "__main__":
    tui = TUI()
    tui.loop()
