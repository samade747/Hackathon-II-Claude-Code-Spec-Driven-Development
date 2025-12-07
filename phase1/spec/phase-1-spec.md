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

- `src/todo/models.py` — Task dataclass.
- `src/todo/storage.py` — In-memory store API:
  - add_task()
  - delete_task()
  - update_task()
  - list_tasks()
  - get_task()
  - search_tasks()
- `src/todo/cli.py` — CLI entrypoint using `argparse` with subcommands.
- `src/todo/utils.py` — helper functions: now_iso(), parse_tags(), validate_priority(), validate_uuid().
- `tests/test_todo.py` — pytest suite covering acceptance tests.

## CLI Behaviour Examples

- `todo add "Buy milk" --description "2 liters" --priority high --tags personal,shopping --due 2025-12-10T09:00:00Z`
- `todo list --filter status=pending --sort due_date --json`
- `todo update <id> --title "New title"`
- `todo delete <id>`
- `todo complete <id>`

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
