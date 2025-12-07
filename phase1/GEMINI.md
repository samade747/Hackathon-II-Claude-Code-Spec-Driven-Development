# GEMINI.md — Optional Gemini Usage

If you also use Gemini CLI for experimentation, you can follow a similar spec-driven flow.

- Use the same specs in `constitution/`, `spec/`, and `tasks/`.
- Request Gemini to generate or refactor code under `src/` and `tests/`.
- Always validate with `pytest -q`.
- Do not mix handwritten production code with generated code; keep specs as the source of truth.
