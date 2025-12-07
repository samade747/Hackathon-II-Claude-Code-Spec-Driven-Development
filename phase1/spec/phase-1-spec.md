# Phase I Specification: Console Todo App

## Objective
Build an in-memory Python console application for managing todo tasks.
All implementation must be produced by your AI tool (Claude Code) using these specs.

## Required Features (Basic)
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark as Complete

## Enhanced Features (Intermediate)
6. Priorities & Tags
7. Search & Filter
8. Sort Tasks

## Data Structure

Use `dataclasses.dataclass` for `Task` model with fields:

- `id: str`  # uuid4
- `title: str`
- `description: Optional[str]`
- `status: Literal['pending','completed']` = 'pending'
- `priority: Optional[Literal['high','medium','low']]` = 'medium'
- `tags: list[str]` = field(default_factory=list)
- `created_at: str`  # ISO 8601 UTC
- `modified_at: Optional[str]`
- `due_date: Optional[str]`

## Modules & Responsibilities

- `src/todo/models.py` — Task dataclass with rich formatting helpers.
- `src/todo/storage.py` — Storage implementations:
  - `InMemoryStorage` — In-memory storage (data lost on exit, per original spec)
  - `FileStorage` — JSON file persistence (data persists across sessions)
  - Both implement same interface for consistency
- `src/todo/cli.py` — CLI entrypoint using `argparse` with subcommands and rich UI.
- `src/todo/utils.py` — helper functions: now_iso(), parse_tags(), validate_priority(), validate_uuid().
- `tests/test_todo.py` — pytest suite covering acceptance tests.

## CLI Behaviour Examples

### Basic Commands
- `python -m src.todo.cli add "Buy milk" --description "2 liters" --priority high --tags personal,shopping --due 2025-12-10T09:00:00Z`
- `python -m src.todo.cli list --filter status=pending --sort due_date`
- `python -m src.todo.cli update <id> --title "New title" --priority high`
- `python -m src.todo.cli delete <id>`
- `python -m src.todo.cli complete <id>`

### Advanced Options
- `python -m src.todo.cli --storage memory list` — Use in-memory storage (data not persisted)
- `python -m src.todo.cli --storage file list` — Use file storage (default, data persisted)
- `python -m src.todo.cli list --format rich` — Rich formatted output with colors and tables (default)
- `python -m src.todo.cli list --format json` — JSON output for scripting
- `python -m src.todo.cli list --format plain` — Plain text output

### Rich UI Features
- Task listings displayed in colorful tables
- Success messages in green with ✓ emoji
- Error messages in red with ✗ emoji
- Status shown with emojis: [ ] pending, [✓] completed
- Priority color-coded: high=red, medium=yellow, low=green
- Interactive TUI mode: `python -m src.agent.tui`


## Acceptance Tests (high-level)

- Adding a task with required fields returns a Task with a uuid and timestamps.
- Adding a task with empty title raises ValueError.
- Deleting a non-existent task raises KeyError.
- Updating a task updates only provided fields.
- Listing returns tasks in creation order by default.
- Search by keyword looks in title and description.
- Filter by status/priority/tags works as described in test-cases.

## Constraints

- No external network calls in tests.
- Minimal dependencies: `pytest` only.
- Deterministic time usage via injectable now() to allow mocking in tests.
