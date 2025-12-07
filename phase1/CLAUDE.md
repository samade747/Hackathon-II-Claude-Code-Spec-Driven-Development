# CLAUDE.md — Using Claude Code for Evolution of Todo (Phase I)

## Prerequisites
- Claude Code installed and configured.
- This repo cloned locally.
- Python 3.11+ and `pytest` available.

## Workflow

1. Read `constitution/CONSTITUTION.md`, `spec/phase-1-spec.md`, and `spec/test-cases.md`.
2. Open Claude Code and point it at this project folder.
3. Use prompts from `history/prompts/001-phase-1.md` or create new ones referencing the specs.
4. Generate code only inside `src/` and `tests/`.
5. After each generation, run:

```bash
pytest -q
```

6. If tests fail, update the spec files (not the generated code) and regenerate.

## Example CLI Command (pseudo)

```bash
claude-code generate --project . --spec spec/phase-1-spec.md --task-file tasks/001-phase-1.task.md
```

Adjust based on your actual Claude Code CLI.
