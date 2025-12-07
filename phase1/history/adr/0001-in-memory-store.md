# ADR 0001 — Use In-memory Store for Phase I

## Context
Phase I focuses on console-based functionality and spec-driven development.
Persistence across runs is not required until Phase II.

## Decision
Use an in-memory list with UUID-based ids and helper functions for CRUD operations.
No external database is used in Phase I.

## Consequences
- Pros:
  - Simple implementation.
  - Fast and deterministic tests.
  - No external infrastructure needed.
- Cons:
  - Data lost when the process ends.
  - Requires migration to a real database in Phase II.
