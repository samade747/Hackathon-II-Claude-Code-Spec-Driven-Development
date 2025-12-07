# Todo App Constitution

## Core Principles
1. **Simplicity First**: Start with minimal viable features.
2. **User-Centric**: All interactions must be intuitive.
3. **Data Integrity**: Never lose user data during a session.
4. **Extensibility**: Design for future AI integration and Phase II.

## Development Standards
- **Python Version**: Use Python 3.11+ with type hints in all code
- **Code Style**: 
  - Follow PEP 8 style guidelines
  - Maximum line length: 100 characters
  - Use meaningful variable and function names
- **Documentation**:
  - All public functions and classes must have docstrings
  - Docstrings should include: summary, Args, Returns, Raises
  - Use Google-style docstring format
  - Add inline comments for complex logic
- **Validation**: Input validation on all user entries
- **Error Handling**: 
  - Graceful error handling with user-friendly messages
  - Use specific exception types
  - Log errors appropriately
  - Never expose stack traces to end users
- **Testing**: 
  - Tests via `pytest` with deterministic behaviour
  - Mock time/external dependencies where needed
  - Aim for >90% code coverage
  - Test both happy paths and error cases
  - Use parametrized tests for multiple scenarios
- **Dependencies**: Keep dependencies minimal and well-justified

## Data Model Principles
- Each task has a unique ID (UUID4 string).
- Timestamps for creation and updates (`created_at`, `modified_at` in ISO 8601 UTC).
- Support for flexible metadata: `priority`, `tags`, and optional `due_date`.

## Success Criteria (Phase I)
- **Testing**: 
  - All acceptance tests in `spec/test-cases.md` pass under `pytest`
  - Minimum 90% code coverage across all modules
  - All edge cases and error conditions tested
  - Integration tests verify end-to-end workflows
- **Code Quality**:
  - Code follows spec-driven development principles
  - All code has type hints and docstrings
  - No linting errors (PEP 8 compliance)
  - Clean architecture with clear separation of concerns
- **Functionality**:
  - All Phase I features implemented and working
  - Both InMemoryStorage and FileStorage supported
  - Rich CLI UI provides excellent user experience
  - Agent system with reusable skills functional
- **Documentation**:
  - Comprehensive `README.md` with usage examples
  - Complete CLI command reference
  - Architecture documentation
  - Development guide for contributors
  - All public APIs documented

## Agentic Capabilities (Phase III+)
- **Autonomy**: Agents may perform file I/O and shell commands only when explicitly authorized or within sandboxed environments.
- **Transparency**: Agents must report their actions and results clearly to the user.
- **Safety**: System-critical operations (deletion, overwriting) require confirmation or revert capabilities.

## UI Standards (Phase IV)
- **Terminal First**: The primary interface is the console.
- **Rich Experience**: Use 
ich library for dashboards.
- **Clarity**: Use colors consistently (Green=Success, Red=Error).
