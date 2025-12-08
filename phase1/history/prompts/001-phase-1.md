# Project Prompt History — Phase I

This document captures the *actual* feel of the conversation used to generate this codebase. It reflects a realistic, iterative dialogue between a human developer and the AI.

## Session 1: The Core App

### Prompt 1: Getting Started
**User:**
"hey, i wanna build a todo app in python.
can you start by making a model for a Task?
put it in `src/todo/models.py`.
it needs an id, title, description, status (pending/completed), priority (high/medium/low), and tags.
oh, and timestamps for when it was created and stuff. use dataclasses."

### Prompt 2: Adding Persistence
**User:**
"cool. now i need to save these.
make a storage module in `src/todo/storage.py`.
i want to be able to save to a json file, but also support in-memory for tests.
can you use a protocol or abstract class so we can swap it later?
supports standard crud: add, get, list (with filters), update, delete."

### Prompt 3: Helper Functions
**User:**
"actually, can you move the timestamp stuff and some validation logic to a utils file?
`src/todo/utils.py`.
need things like `now_iso()` and something to validate that the priority is actually one of the allowed values. also maybe a helper to parse tags from a string."

### Prompt 4: The CLI
**User:**
"okay lets make a CLI to test this out.
`src/todo/cli.py`.
use argparse. commands: add, list, complete, delete.
for the list command, can you make it look nice? maybe use that `rich` library to print a table?
i want to see the status emoji and color-coded priorities."

## Session 2: The Agent Framework

### Prompt 5: Basic Agent Structures
**User:**
"alright, the todo app works. now for the cool part. i want to wrap this in an agent system.
create `src/agent/base.py`.
i need a `Skill` class that wraps a python function, and an `Agent` class that has a name, a persona (system prompt), and a list of skills.
the agent needs a `run` method that takes user input."

### Prompt 6: Making Skills
**User:**
"now let's turn the todo functions into skills the agent can use.
create `src/agent/skills.py`.
basically just wrap the storage methods (add, list, etc) but make them return nice strings that the agent can understand. like 'Task added with ID 123' instead of the object."

### Prompt 7: System Access
**User:**
"i want the agent to be able to read files and run shell commands too.
put that in `src/agent/sys_skills.py`.
be careful though, add a big warning to the shell command one.
implement read, write, list dir, and run command."

### Prompt 8: The Manager
**User:**
"okay let's build the actual agents. `src/agent/manager.py`.
create a `TodoManager` agent that uses the todo skills. give it a persona like 'helpful productivity assistant'.
and a `SysAdminAgent` that uses the sys skills. persona: 'strict sysadmin'.
write a simple run method that checks the command and calls the right skill."

## Session 3: Going Advanced

### Prompt 9: Cloud Blueprints
**User:**
"i want to add some 'visionary' agents later.
start by creating `src/agent/cloud_skills.py`.
these shouldn't actually touch the cloud yet, just generate code.
like `generate_k8s_manifest`, `generate_terraform`, `generate_docker_compose`.
just return the code as a string."

### Prompt 10: MCP Stuff
**User:**
"have you heard of MCP? Model Context Protocol?
mock up a client for it in `src/agent/mcp_integration.py`.
just simulate connecting to a server and listing tools. i want my agent to be able to 'connect' to external tools later."

### Prompt 11: The Visionaries
**User:**
"now create `src/agent/advanced_agents.py`.
i want three high-level agents:
1. CloudArchitect: uses the cloud skills. super visionary persona.
2. MCPIntegrationAgent: uses the mcp client.
3. IntelligenceOrchestrator: this one manages patterns and workflows.
give them really flowery, impressive personas."

### Prompt 12: The TUI
**User:**
"last thing. the cli is boring.
make a real TUI in `src/agent/tui.py`.
use `rich.layout`. i want a header, a main chat window, and a footer.
make it interactive so i can chat with the agents.
green panels for success messages, red for errors. make it look pro."
