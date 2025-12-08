"""
Enhanced Terminal User Interface (TUI) with Rich formatting.
Professional, easy-to-use interactive interface for todo management.
"""
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.live import Live
from rich import box
import time

from src.agent.manager import TodoManager, SysAdminAgent


class EnhancedTUI:
    """
    Enhanced Terminal User Interface (TUI) for the Todo Application.
    
    This class manages the interactive session, rendering a beautiful
    command-line interface using the 'rich' library. It maintains the
    application state (active agent, chat history) and handles the main
    event loop.
    """
    
    def __init__(self):
        """Initialize TUI components, agents, and state."""
        self.console = Console()
        self.todo_agent = TodoManager()
        self.sys_agent = SysAdminAgent()
        self.current_agent = self.todo_agent
        self.chat_history = []
        self.running = True
        self.show_welcome()
    
    def show_welcome(self):
        """Display welcome message with instructions."""
        self.console.clear()
        welcome = Panel(
            Text.from_markup(
                """[bold cyan]🚀 Evolution of Todo - Enhanced Interactive TUI[/bold cyan]

[green]✓ Easy Commands - Just type naturally![/green]
[yellow]📝 Examples:[/yellow]
  • [cyan]add Buy groceries[/cyan] - Add a task
  • [cyan]list[/cyan] - Show all tasks
  • [cyan]search milk[/cyan] - Find tasks
  • [cyan]stats[/cyan] - View statistics
  • [cyan]complete <id>[/cyan] - Mark task done
  • [cyan]delete <id>[/cyan] - Remove task
  • [cyan]help[/cyan] - Show all commands
  • [cyan]clear[/cyan] - Clear screen
  • [cyan]exit[/cyan] - Quit TUI

[dim]Type your command below...[/dim]"""
            ),
            title="Welcome to Enhanced TUI",
            border_style="bold cyan",
            padding=(1, 2)
        )
        self.console.print(welcome)
        self.console.print()
    
    def create_interface(self) -> Layout:
        """
        Creates the main three-pane layout (Header, Main, Footer).
        
        Returns:
            Layout: The root layout object ready for rendering.
        """
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["header"].update(self.render_header())
        layout["main"].update(self.render_main())
        layout["footer"].update(self.render_footer())
        
        return layout
    
    def render_header(self) -> Panel:
        """Render header with agent info."""
        title = Text()
        title.append("🤖 ", style="bold")
        title.append(f"Active Agent: {self.current_agent.name}", style="bold cyan")
        title.append(" | ", style="dim")
        title.append("Type 'help' for commands", style="yellow")
        
        return Panel(
            title,
            style="bold white on blue",
            box=box.HEAVY
        )
    
    def render_main(self) -> Panel:
        """Render main content area."""
        if not self.chat_history:
            content = Text("No messages yet. Type a command to get started!", style="dim italic")
        else:
            # Show last 15 messages
            lines = []
            for msg in self.chat_history[-15:]:
                lines.append(msg)
            content = "\n".join(lines)
        
        return Panel(
            content,
            title="💬 Chat History",
            border_style="green",
            padding=(1, 2)
        )
    
    def render_footer(self) -> Panel:
        """Render footer with quick tips."""
        tips = Text()
        tips.append("💡 Quick Tips: ", style="bold yellow")
        tips.append("add <task> ", style="cyan")
        tips.append("| ", style="dim")
        tips.append("list ", style="cyan")
        tips.append("| ", style="dim")
        tips.append("stats ", style="cyan")
        tips.append("| ", style="dim")
        tips.append("help ", style="cyan")
        tips.append("| ", style="dim")
        tips.append("exit", style="red")
        
        return Panel(tips, style="bold white on black")
    
    def show_help(self):
        """Show comprehensive help."""
        help_table = Table(
            title="📚 All Available Commands",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            box=box.ROUNDED
        )
        help_table.add_column("Command", style="cyan", width=20)
        help_table.add_column("Description", style="white", width=40)
        help_table.add_column("Example", style="yellow", width=30)
        
        commands = [
            ("add <task>", "Add a new task", "add Buy groceries"),
            ("list", "Show all tasks", "list"),
            ("list pending", "Show pending tasks", "list pending"),
            ("list completed", "Show completed tasks", "list completed"),
            ("search <query>", "Find tasks", "search milk"),
            ("complete <id>", "Mark task as done", "complete a1b2c3"),
            ("delete <id>", "Remove a task", "delete a1b2c3"),
            ("details <id>", "View task details", "details a1b2c3"),
            ("stats", "View statistics", "stats"),
            ("help", "Show this help", "help"),
            ("clear", "Clear the screen", "clear"),
            ("switch", "Switch to SysAdmin agent", "switch"),
            ("exit", "Exit the TUI", "exit"),
        ]
        
        for cmd, desc, example in commands:
            help_table.add_row(cmd, desc, example)
        
        self.console.print()
        self.console.print(help_table)
        self.console.print()
    
    def show_tasks_table(self, tasks_output: str):
        """Display tasks in a beautiful table."""
        if "No tasks" in tasks_output:
            self.console.print(Panel(
                "📭 No tasks found. Add your first task with: [cyan]add <task name>[/cyan]",
                style="yellow",
                border_style="yellow"
            ))
            return
        
        # Parse the output and create a table
        self.console.print()
        self.console.print(Panel(tasks_output, title="📋 Your Tasks", border_style="green"))
        self.console.print()
    
    def add_to_history(self, user_msg: str, agent_response: str):
        """Add interaction to chat history."""
        self.chat_history.append(f"[bold cyan]You:[/bold cyan] {user_msg}")
        
        # Format response based on content
        if "✓" in agent_response or "successfully" in agent_response.lower():
            self.chat_history.append(f"[bold green]Agent:[/bold green] {agent_response}")
        elif "Error" in agent_response or "✗" in agent_response:
            self.chat_history.append(f"[bold red]Agent:[/bold red] {agent_response}")
        else:
            self.chat_history.append(f"[bold white]Agent:[/bold white] {agent_response}")
    
    def process_command(self, user_input: str):
        """
        Process a single command from the user.
        
        Handles:
        - Meta-commands (help, clear, exit, switch)
        - Agent dispatch (sending input to the active agent)
        - Output formatting (rendering tables, panels, success/error messages)
        - History updates
        
        Args:
            user_input (str): The raw command string typed by the user.
        """
        user_input = user_input.strip()
        
        if not user_input:
            return
        
        # Special commands
        if user_input.lower() == "help":
            self.show_help()
            return
        
        if user_input.lower() == "clear":
            self.console.clear()
            self.show_welcome()
            return
        
        if user_input.lower() in ["exit", "quit", "q"]:
            self.running = False
            self.console.print()
            self.console.print(Panel(
                "[bold green]👋 Thanks for using Evolution of Todo![/bold green]\n"
                "[cyan]All your tasks are saved. Come back anytime![/cyan]",
                title="Goodbye!",
                border_style="cyan"
            ))
            self.console.print()
            return
        
        if user_input.lower() == "switch":
            if self.current_agent == self.todo_agent:
                self.current_agent = self.sys_agent
                msg = "🔄 Switched to SysAdmin Agent"
            else:
                self.current_agent = self.todo_agent
                msg = "🔄 Switched to TodoManager Agent"
            
            self.console.print(Panel(msg, style="yellow"))
            return
        
        # Execute command with agent
        try:
            response = self.current_agent.run(user_input)
            
            # Special handling for list command - show in table
            if user_input.lower().startswith("list"):
                if "No tasks" in response:
                    self.console.print()
                    self.console.print(Panel(
                        "📭 [yellow]No tasks found.[/yellow]\n\n"
                        "💡 Add your first task: [cyan]add Buy groceries[/cyan]",
                        title="Tasks",
                        border_style="yellow"
                    ))
                else:
                    self.console.print()
                    self.console.print(Panel(response, title="📋 Your Tasks", border_style="green", padding=(1, 2)))
                self.console.print()
            
            # Special handling for stats
            elif user_input.lower() in ["stats", "statistics", "summary"]:
                self.console.print()
                self.console.print(Panel(response, title="📊 Statistics", border_style="cyan", padding=(1, 2)))
                self.console.print()
            
            # Special handling for details
            elif user_input.lower().startswith("details") or user_input.lower().startswith("info"):
                self.console.print()
                self.console.print(Panel(response, title="📝 Task Details", border_style="blue", padding=(1, 2)))
                self.console.print()
            
            # Success messages (add, complete, delete, update)
            elif any(word in response for word in ["added", "completed", "deleted", "updated", "Task"]) and "Error" not in response:
                self.console.print()
                self.console.print(f"[bold green]✓ {response}[/bold green]")
                self.console.print()
            
            # Error messages
            elif "Error" in response or "not found" in response.lower() or "required" in response.lower():
                self.console.print()
                self.console.print(f"[bold red]✗ {response}[/bold red]")
                self.console.print()
            
            # Search results
            elif user_input.lower().startswith("search") or user_input.lower().startswith("find"):
                self.console.print()
                self.console.print(Panel(response, title="🔍 Search Results", border_style="yellow", padding=(1, 2)))
                self.console.print()
            
            # Default
            else:
                self.console.print()
                self.console.print(response)
                self.console.print()
            
            # Add to history
            self.add_to_history(user_input, response)
            
        except Exception as e:
            error_msg = f"Error executing command: {e}"
            self.console.print(f"\n[bold red]✗ {error_msg}[/bold red]\n")
            self.add_to_history(user_input, error_msg)
    
    def run(self):
        """
        Starts the main event loop.
        
        Continuously prompts for user input and processes commands
        until the user exits or interrupts.
        """
        try:
            while self.running:
                # Get user input with styled prompt
                try:
                    user_input = Prompt.ask(
                        "\n[bold cyan]>>[/bold cyan]",
                        console=self.console
                    )
                    
                    self.process_command(user_input)
                    
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Press Ctrl+C again or type 'exit' to quit[/yellow]")
                    continue
                except EOFError:
                    break
        
        except KeyboardInterrupt:
            self.console.print("\n[bold green]👋 Goodbye![/bold green]")
        
        finally:
            # Clean exit
            pass


def main():
    """Launch the Enhanced TUI."""
    tui = EnhancedTUI()
    tui.run()


if __name__ == "__main__":
    main()
