# Subagent: todo-core

## Purpose
This subagent is the primary domain expert for Todo task management in Phase I.
It focuses on:
- Task data model and business logic
- In-memory and file-based storage implementations
- Task manipulation operations (CRUD)
- Search, filter, and sort capabilities
- Business rules (validation, status transitions, timestamps)

## Capabilities
- **Interpret specifications**: Reads `tasks/*.task.md` and `spec/*.md` files to understand requirements
- **Generate Python modules**: Creates production code in `src/todo/` following the constitution
- **Ensure test coverage**: All generated code passes tests in `tests/` per `spec/test-cases.md`
- **Handle storage backends**: Implements both InMemoryStorage and FileStorage with identical interfaces
- **Rich UI integration**: Supports rich formatting helpers for enhanced CLI experience

## Skills & Functions
1. **add_task**: Create new tasks with validation
2. **list_tasks**: Retrieve and display tasks with formatting
3. **update_task**: Modify task fields with versioning
4. **delete_task**: Remove tasks with confirmation
5. **search_tasks**: Query tasks by multiple criteria
6. **complete_task**: Mark tasks as done
7. **get_task_details**: View comprehensive task information
8. **get_statistics**: Analyze task metrics

## Generation Patterns
- Use dataclasses for models with type hints
- Implement storage as classes with common interface
- Follow dependency injection for testability
- Mock time in tests for determinism
- Use pytest fixtures for setup/teardown

## Boundaries
- **No database**: Phase I uses in-memory or JSON file storage only
- **No network**: No external API calls or web servers
- **No GUI**: Console-only interface (CLI + TUI)
- **No authentication**: Single-user, local-only

## Quality Standards
- Type hints on all functions
- Docstrings (Google style) on all public APIs
- PEP 8 compliance
- >90% test coverage
- Error handling with user-friendly messages
