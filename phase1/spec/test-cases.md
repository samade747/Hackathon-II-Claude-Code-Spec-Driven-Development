# Phase I Test Cases

## Test 1: Add Tasks
1. Add task "Buy groceries" with priority "high" and tag "personal".
2. Add task "Finish report" with priority "medium" and tag "work".
3. Verify both appear in task list; count == 2.

## Test 2: Update Task
1. Update first task title to "Buy groceries and cook dinner".
2. Verify change appears in list.

## Test 3: Mark Complete
1. Mark first task as complete.
2. Verify status shows "completed".

## Test 4: Filter by status
1. Filter by status: completed.
2. Should show only completed tasks.

## Test 5: Search
1. Search for "report".
2. Should show "Finish report" task.

## Test 6: Delete
1. Delete completed task.
2. Verify it no longer appears.

## Test 7: Sort
1. Sort tasks by priority.
2. Verify order: high, medium, low.

## Test 8: Rich UI Output
1. List tasks with rich formatting enabled.
2. Verify output contains ANSI color codes.
3. Verify table formatting is present.

## Test 9: Storage Backend - InMemory
1. Use InMemoryStorage for operations.
2. Add, update, complete tasks.
3. Verify all operations work correctly.

## Test 10: Storage Backend - File
1. Use FileStorage for operations.
2. Add tasks, restart storage.
3. Verify tasks persist across sessions.

## Test 11: Agent Skills
1. Use TodoManager agent to add task.
2. Use agent to list tasks.
3. Use agent to complete task.
4. Verify agent skills work correctly.

## Test 12: Multiple Filters
1. Add tasks with various attributes.
2. Filter by status AND priority.
3. Filter by tags AND status.
4. Verify combined filters work correctly.
