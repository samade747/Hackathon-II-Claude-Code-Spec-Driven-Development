# Project Prompt History — Phase I

This document captures the conversational prompts used to build the system from scratch.

## 1. The Foundation: Data Models
**User:**
"Let's start building the Todo application. I need a solid data model to begin with.
Create `src/todo/models.py` with a `Task` dataclass.
It should have:
- A UUID `id` generated automatically.
- `title` and `description`.
- `status` (defaulting to pending) and `priority` (high/medium/low).
- A list of `tags`.
- Timestamps for creation, modification, and due dates.
Also, add some helper methods like `to_dict()` for saving, and `get_status_emoji()` because we'll want a nice UI later. Use Python's `dataclasses`."

## 2. Storage Layer
**User:**
"Great. Now we need a way to save these tasks.
Create `src/todo/storage.py`.
I want an abstract protocol called `StorageProtocol` so we can swap backends.
Then implement two versions:
1. `InMemoryStorage` for our tests.
2. `FileStorage` that saves to a JSON file (default to `tasks.json`).
Implement standard CRUD methods: `add_task`, `get_task`, `update_task`, `delete_task`, `list_tasks`, and a `search_tasks` that can filter by query or tags."

## 3. Utilities
**User:**
"I see we need some helper functions for timestamps and validation.
Create `src/todo/utils.py`.
Add functions to:
- Get the current time in ISO format (`now_iso`).
- Validate priority strings.
- Validate UUIDs.
- Parse a comma-separated string of tags into a list.
Make sure to add docstrings so we know how to use them."

## 4. The CLI
**User:**
"Let's build a simple interface to test this.
Create `src/todo/cli.py` using `argparse`.
It needs commands for `add`, `list`, `update`, `delete`, and `complete`.
For the `list` command, use the `rich` library to print a nice table with columns for Status, Title, Priority, and Due Date.
Also support global flags like `--storage memory` or `--format json`."

## 5. Agent Architecture
**User:**
"Okay, the core app is working. Now let's build the Agent framework.
Create `src/agent/base.py`.
I need two main classes:
1. `Skill`: This should wrap a python function. It needs a name, description, and a way to inspect the function's parameters automatically.
2. `Agent`: This will be our base class. It has a name, a `persona` (which is just a system prompt string), and a list of `Skill`s. It needs an abstract `run(user_input)` method."

## 6. Basic Skills
**User:**
"Now let's bridge the Todo app to the Agent.
Create `src/agent/skills.py`.
I want you to wrap the `FileStorage` methods into simple, agent-friendly functions.
Create functions like `add_task`, `list_tasks`, `complete_task` that take string inputs and return string messages (e.g., 'Task added successfully').
These will be the tools our agent uses."

## 7. System Skills
**User:**
"I want the agent to be able to do some system admin work too.
Create `src/agent/sys_skills.py`.
Add skills for `read_file`, `write_file`, `list_directory`, and `run_shell_command`.
**Important**: Add a warning docstring to `run_shell_command` saying it's high-risk. We don't want the agent deleting things accidentally."

## 8. The Manager Agent
**User:**
"Let's create our first actual agents in `src/agent/manager.py`.
First, `TodoManager`. Give it a persona of a 'helpful productivity partner'. It should be able to look at user input and decide which skill from `skills.py` to call.
Second, `SysAdminAgent`. Give it a persona of a 'meticulous system administrator'. It should use the skills from `sys_skills.py`.
Implement a matching logic (like checking the first word of the command) to route the request to the right function."

## 9. Visionary Agents: Cloud Architect
**User:**
"Now I want to get fancy. Let's create some 'Visionary' agents for advanced tasks.
First, we need the skills. Create `src/agent/cloud_skills.py`.
These shouldn't actually provision cloud resources (that's too dangerous for now), but they should generate *blueprints*.
Write functions like `generate_kubernetes_deployment`, `generate_docker_compose`, and `generate_terraform_module`.
They should take parameters like `app_name` or `replicas` and return a string containing the YAML or HCL code."

## 10. MCP Integration
**User:**
"I want this agent to be compatible with the Model Context Protocol (MCP).
Create `src/agent/mcp_integration.py`.
Build a mock `MCPClient` class. It doesn't need to be fully functional yet, but simulate methods for `connect_server`, `list_resources`, and `invoke_tool`.
Make it simulate a connection where it discovers some dummy resources and tools so we can test the interface."

## 11. Advanced Agents Implementation
**User:**
"Now create `src/agent/advanced_agents.py` to house these new personas.
I want:
1. `CloudArchitectAgent`: The 'visionary builder'. It uses the cloud skills to generate infrastructure code.
2. `MCPIntegrationAgent`: The 'universal adapter'. It uses the MCP client to talk to external tools.
3. `IntelligenceOrchestratorAgent`: The 'conductor'. It doesn't do work itself but manages workflows and patterns.
Give them really descriptive, inspiring docstrings and personas."

## 12. The Enhanced TUI
**User:**
"Finally, let's tie it all together with a professional UI.
Create `src/agent/tui.py`.
I want a 3-pane layout using `rich.layout`: Header (agent status), Main (chat history), and Footer (tips).
It should be an interactive loop.
- Allow typing commands like 'add ...' or 'switch' to change agents.
- Show agent responses in colored panels (Green for success, Red for error).
- Make it look premium and modern."
