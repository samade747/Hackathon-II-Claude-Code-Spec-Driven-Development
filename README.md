# Evolution of Todo — Phase I: Pro-Level CLI Todo App

[![Tests](https://img.shields.io/badge/tests-49%20passing-brightgreen)](./tests/) [![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/) [![Rich](https://img.shields.io/badge/ui-rich-purple)](https://github.com/Textualize/rich)

A **professional-grade**, spec-driven CLI todo application showcasing the full capabilities of Claude Code agents and subagents with an exceptional terminal UI powered by the `rich` library.

## ✨ Features

### Core Todo Management
- ✅ **CRUD Operations**: Add, view, update, delete tasks
- 🔍 **Advanced Search**: Search tasks by title, description, tags, priority, or status
- 📊 **Statistics Dashboard**: Real-time analytics of your tasks
- 🏷️ **Rich Metadata**: Priorities, tags, due dates, descriptions
- 💾 **Dual Storage**: Choose between in-memory (volatile) or file-based (persistent) storage

###🎨 Pro-Level CLI UI
- 🌈 **Rich Formatting**: Beautiful tables, panels, and colored output
- 🎭 **Multiple Output Formats**: Rich (default), plain text, or JSON
- ✓ **Status Indicators**: Emojis and colors for visual feedback
- 📱 **Responsive**: Adapts to terminal width
- 🤖 **Interactive TUI**: Full-screen terminal UI with live updates

### 🧠 AI-Ready Agent System
- 🎯 **Reusable Skills**: 8 modular, testable capabilities
- 🤝 **Multiple Agents**: TodoManager and SysAdmin agents
- 🔌 **Extensible**: Easy to add new skills and agents
- 📚 **Well-Documented**: Comprehensive docstrings and type hints
- 🔄 **Natural Language**: Command aliases (add/create/new, list/show/ls, etc.)

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to the repository
cd d:\github\Hackathon-II-Claude-Code-Spec-Driven-Development\phase1

# Install dependencies
pip install -r requirements.txt

# Run tests to verify installation
pytest -q
```

### Basic Usage

```bash
# Add a task (with rich formatting)
python -m src.todo.cli add "Buy groceries" --priority high --tags "shopping,personal"

# List all tasks (beautiful table view)
python -m src.todo.cli list

# List with filters
python -m src.todo.cli list --filter status=pending

# Update a task  
python -m src.todo.cli update <task-id> --priority medium --description "Updated description"

# Mark task as complete
python -m src.todo.cli complete <task-id>

# Delete a task
python -m src.todo.cli delete <task-id>
```

### Advanced Features

```bash
# Use in-memory storage (data not persisted)
python -m src.todo.cli --storage memory list

# JSON output for scripting
python -m src.todo.cli --format json list

# Plain text output (no colors)
python -m src.todo.cli --format plain list

# Launch interactive TUI mode
python -m src.agent.tui
```

## 📊 Agent System

### TodoManager Agent

Professional task management agent with 8 skills:
- `add_task` - Create tasks with validation
- `list_tasks` - Display tasks with filters
- `search_tasks` - Find tasks by query
- `update_task` - Modify task fields
- `delete_task` - Remove tasks
- `complete_task` - Mark as done
- `get_task_details` - View full task info
- `get_statistics` - Task analytics

**Natural Language Commands**: The TodoManager understands aliases like:
- `add`/`create`/`new` for adding tasks
- `list`/`show`/`ls` for listing
- `search`/`find` for searching
- `complete`/`done`/`finish` for marking complete
- `delete`/`remove`/`rm` for deletion
- `details`/`info`/`view` for detailed view
- `stats`/`statistics`/`summary` for analytics

### TUI (Terminal User Interface)

```bash
python -m src.agent.tui
```

Features:
- 📋 Live task list with statistics
- 💬 Chat history with agent
- 🔄 Switch between agents (todo/sysadmin)
- ⌨️ Keyboard-driven interface

## 📁 Project Structure

```
phase1/
├── constitution/          # Project constitution & standards
│   └── CONSTITUTION.md   # Development standards, UI guidelines, agent principles
├── spec/                  # Technical specifications
│   ├── phase-1-spec.md   # Phase I functional spec
│   └── test-cases.md     # Test scenarios
├── .specify/              # Subagent definitions
│   ├── context.md        # Project context
│   └── subagents/
│       └── todo-core.subagent.md  # Todo domain expert
├── src/
│   ├── todo/              # Core todo implementation
│   │   ├── models.py     # Task dataclass with rich helpers
│   │   ├── storage.py    # InMemoryStorage & FileStorage
│   │   ├── cli.py        # Rich CLI with storage selection
│   │   └── utils.py      # Helper functions
│   └── agent/             # AI agent system
│       ├── base.py       # Agent & Skill base classes
│       ├── manager.py    # TodoManager & SysAdminAgent
│       ├── skills.py     # Reusable todo skills
│       ├── sys_skills.py # System-level skills
│       └── tui.py        # Terminal UI
├── tests/                 # Test suite (49 tests, 100% passing)
└── requirements.txt       # Dependencies
```

## 🧪 Testing

```bash
# Run all tests
pytest -q

# Verbose output with coverage
pytest -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_todo.py -v
```

**Test Coverage**: 49 tests covering:
- ✅ Task model creation and validation
- ✅ Storage backends (InMemory & File)
- ✅ CLI commands
- ✅ Search and filter operations
- ✅ Agent skills
- ✅ Error handling

## 🎨 Rich UI Examples

### Task List (Rich Format)
```
                    📋 Tasks                         
┏━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┓
┃ ✓ ┃ Title            ┃ Priority ┃ Tags    ┃ Due Date   ┃ ID     ┃
┡━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━┩
│   │ Buy groceries    │ high     │ shop... │ 2025-12-10 │ a1b2c3 │
│ ✓ │ Walk the dog     │ medium   │ person..│            │ d4e5f6 │
└───┴──────────────────┴──────────┴─────────┴────────────┴────────┘
```

### Success/Error Messages
- ✓ Success messages in green
- ✗ Error messages in red
- ⚠ Warnings in yellow
- ℹ Info in blue

## 🏗️ Architecture

### Spec-Driven Development
All code is generated following specifications in `constitution/` and `spec/` directories. This ensures:
- Consistency across implementations
- Clear requirements
- Testable behavior
- Easy onboarding

### Agent-Based Design
The application uses a skill-based agent architecture:
1. **Skills**: Atomic, reusable capabilities
2. **Agents**: Collections of skills with specific personas
3. **Managers**: Orchestrate skills to handle user requests

### Storage Abstraction
Two storage backends share a common interface:
- **InMemoryStorage**: Fast, volatile (Phase I spec-compliant)
- **FileStorage**: Persistent JSON storage

## 📚 Development

### Adding a New Skill

1. Define skill function in `src/agent/skills.py`:
```python
def my_new_skill(param: str) -> str:
    """Skill description with type hints."""
    # Implementation
    return result
```

2. Add to agent in `src/agent/manager.py`:
```python
self.add_skill(Skill.from_callable(skills.my_new_skill))
```

3. Write tests in `tests/test_agent_skills.py`

### Adding a New Agent

See `src/agent/manager.py` for examples of TodoManager and SysAdminAgent.

## 📖 Documentation

- [Constitution](./constitution/CONSTITUTION.md) - Development standards & principles
- [Phase I Spec](./spec/phase-1-spec.md) - Functional specification
- [Test Cases](./spec/test-cases.md) - Test scenarios
- [Todo-Core Subagent](./specify/subagents/todo-core.subagent.md) - Domain expert definition

## 💡 Design Principles

1. **Simplicity First**: Start minimal, extend deliberately
2. **User-Centric**: Intuitive interactions
3. **Data Integrity**: Never lose user data
4. **Extensibility**: Design for AI integration
5. **Quality**: >90% test coverage, PEP 8 compliant
6. **Rich UX**: Professional terminal experience

## 🎯 Success Criteria

- ✅ 49/49 tests passing
- ✅ >90% code coverage
- ✅ All Phase I features implemented
- ✅ Both storage backends working
- ✅ Rich CLI UI implemented
- ✅ Agent system functional
- ✅ Comprehensive documentation
- ✅ PEP 8 compliant

## 🚀 Next Steps (Phase II+)

- Phase II: Web app with FastAPI/Next.js/Neon
- Phase III: AI chatbot with Agents/MCP
- Phase IV-V: Kubernetes & cloud deployment

## 📄 License

This project is part of the Evolution of Todo hackathon demonstrating spec-driven development with Claude Code.

---

**Built with ❤️ using Claude Code, Rich, and Python 3.11+**
