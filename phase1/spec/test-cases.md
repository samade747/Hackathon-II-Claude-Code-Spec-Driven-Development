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
