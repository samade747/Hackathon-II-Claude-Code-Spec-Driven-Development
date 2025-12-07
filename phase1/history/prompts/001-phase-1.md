# Prompt History — Phase I

## Prompt 1 — Data Model
Ask Claude Code:

"""text
Implement a Python dataclass `Task` in `src/todo/models.py` with the fields and behaviour described in `spec/phase-1-spec.md` (Data Structure section). Include a `to_dict()` method and basic validation for title, priority, and status. Create tests in `tests/test_models.py`.
"""

## Prompt 2 — Storage
Ask Claude Code:

"""text
Implement an in-memory storage module in `src/todo/storage.py` with add_task, delete_task, update_task, list_tasks, get_task, search_tasks, and filter/sort helpers as described in `spec/phase-1-spec.md` and `spec/test-cases.md`. Create tests in `tests/test_storage.py`.
"""

(Add more prompts here as you iterate.)
