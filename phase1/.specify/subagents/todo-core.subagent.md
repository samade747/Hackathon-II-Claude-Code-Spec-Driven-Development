# Subagent: todo-core

## Purpose
This subagent focuses on core Todo domain logic for Phase I:
- Task model
- In-memory storage
- Business rules (validation, status transitions)

## Capabilities
- Interpret tasks/*.task.md specs.
- Generate Python modules under src/todo/.
- Ensure tests in tests/ pass according to spec/test-cases.md.

## Boundaries
- No database or network code.
- No web server or GUI (console-only).
