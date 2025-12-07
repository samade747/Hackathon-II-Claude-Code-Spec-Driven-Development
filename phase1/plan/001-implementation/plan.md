# Plan 001 — Phase I Implementation

## Milestones

- M1: Data model & utils
  - Generate `models.py` and `utils.py`.
  - Add basic tests for Task creation and validation.

- M2: Storage
  - Generate `storage.py` with CRUD and search/filter/sort.
  - Add tests ensuring behaviour matches spec/test-cases.

- M3: CLI
  - Generate `cli.py` wiring subcommands to storage.
  - Support interactive and argument-based mode.

- M4: Polish & Docs
  - JSON output (`--json`).
  - Update README and example usage.
  - Final test run and clean-up.

## Workflow

After each milestone:

1. Run `pytest -q`.
2. If failures occur, update spec files (not code).
3. Re-run Claude Code for the affected modules only.
