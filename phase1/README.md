# Evolution of Todo — Phase I: Ultra-Advanced AI-Powered CLI Todo App

[![Tests](https://img.shields.io/badge/tests-49%20passing-brightgreen)](./tests/) [![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/) [![Rich](https://img.shields.io/badge/ui-rich-purple)](https://github.com/Textualize/rich) [![MCP](https://img.shields.io/badge/MCP-integrated-orange)](https://modelcontextprotocol.io)

A **next-generation**, production-ready CLI todo application featuring **MCP integration**, **reusable intelligence patterns**, **cloud-native blueprint generation**, and exceptional terminal UI powered by AI agents.

---

## 🚀 Quick Start (60 seconds)

### Step 1: Navigate to phase1 directory
```bash
cd phase1
```

### Step 2: Run the TUI
```bash
python -m src.agent.tui
```

**OR use the launcher scripts:**
```bash
# PowerShell (Windows)
.\launch-tui.ps1

# Bash (Linux/Mac)
./launch-tui.sh
```

### Step 3: Try commands in TUI
```
add Buy groceries
list
stats
help
exit
```

---

## 📋 All Commands Must Run from phase1 Directory!

**IMPORTANT:** All commands below assume you're in the `phase1` directory:
```bash
cd d:\github\Hackathon-II-Claude-Code-Spec-Driven-Development\phase1
```

---

## ✨ Features

### 🎯 Core Todo Management
- ✅ Full CRUD: Add, list, update, delete, complete tasks
- 🔍 Advanced Search: By query, status, priority, tags
- 📊 Statistics: Real-time task analytics
- 💾 Dual Storage: InMemory (volatile) or File (persistent)
- 🎨 Rich UI: Tables, colors, emojis
- 📤 Multiple Formats: Rich, plain, JSON

### 🤖 AI Agent System
- **5 Specialized Agents**: TodoManager, SysAdmin, CloudArchitect, MCPIntegrator, IntelligenceOrchestrator
- **20+ Skills**: Modular, reusable capabilities
- **Natural Language**: Command aliases
- **Multi-Agent**: Collaboration

### ☁️ Cloud-Native
- 🏗️ Kubernetes manifests
- 🐳 Docker Compose
- 🔧 Terraform modules
- 🔄 CI/CD pipelines
- 📊 Monitoring stacks
- 💰 Cost estimation

### 🌐 MCP Integration
- 📡 Server connectivity
- 📚 Resource access
- 🛠️ Tool invocation
- 📝 Prompt templates

### 🧠 Reusable Intelligence
- 📋 Intelligence patterns
- 🔗 Skill composition
- 📚 Knowledge base

---

## 🎬 Core Todo Commands

**All commands from `phase1` directory:**

```bash
# Add task
python -m src.todo.cli add "My task" --priority high

# List tasks
python -m src.todo.cli list

# Update task
python -m src.todo.cli update <task-id> --priority medium

# Complete task
python -m src.todo.cli complete <task-id>

# Delete task
python -m src.todo.cli delete <task-id>

# JSON output
python -m src.todo.cli --format json list

# InMemory storage
python -m src.todo.cli --storage memory add "Temp task"
```

---

## ☁️ Cloud-Native Blueprints

**Generate Kubernetes:**
```bash
python -c "from src.agent.advanced_agents import CloudArchitectAgent; print(CloudArchitectAgent().run('k8s todo-app nginx:latest'))"
```

**Generate Docker Compose:**
```bash
python -c "from src.agent.advanced_agents import CloudArchitectAgent; print(CloudArchitectAgent().run('docker'))"
```

**Generate CI/CD Pipeline:**
```bash
python -c "from src.agent.advanced_agents import CloudArchitectAgent; print(CloudArchitectAgent().run('cicd myapp'))"
```

**Generate Monitoring Stack:**
```bash
python -c "from src.agent.advanced_agents import CloudArchitectAgent; print(CloudArchitectAgent().run('monitoring'))"
```

**Estimate Costs:**
```bash
python -c "from src.agent.advanced_agents import CloudArchitectAgent; print(CloudArchitectAgent().run('cost'))"
```

---

## 🌐 MCP Integration

**Connect to Server:**
```bash
python -c "from src.agent.advanced_agents import MCPIntegrationAgent; agent = MCPIntegrationAgent(); print(agent.run('connect kb http://localhost:3000')); print(agent.run('status'))"
```

**List Resources:**
```bash
python -c "from src.agent.advanced_agents import MCPIntegrationAgent; agent = MCPIntegrationAgent(); agent.run('connect kb http://localhost:3000'); print(agent.run('resources'))"
```

---

## 🧠 Intelligence Patterns

**List Patterns:**
```bash
python -c "from src.agent.advanced_agents import IntelligenceOrchestratorAgent; print(IntelligenceOrchestratorAgent().run('patterns'))"
```

**Compose Skills:**
```bash
python -c "from src.agent.advanced_agents import IntelligenceOrchestratorAgent; print(IntelligenceOrchestratorAgent().run('compose search_tasks,add_task,update_task workflow1'))"
```

---

## 🧪 Testing

```bash
# From phase1 directory
pytest -q

# Expected: 49 passed
```

---

## 🎯 Available Agents

1. **TodoManager** - 8 core task skills
2. **CloudArchitect** - 6 cloud blueprint skills
3. **MCPIntegrator** - 6 MCP connectivity skills
4. **IntelligenceOrchestrator** - 7 intelligence skills
5. **SysAdminAgent** - System operations

---

## 📁 Project Structure

```
phase1/                          ← YOU MUST BE HERE!
├── src/
│   ├── todo/
│   │   ├── cli.py              ← Main CLI
│   │   ├── models.py
│   │   └── storage.py
│   └── agent/
│       ├── tui.py              ← Terminal UI
│       ├── advanced_agents.py  ← Cloud, MCP, Intelligence agents
│       ├── cloud_skills.py
│       ├── mcp_integration.py
│       └── intelligence_orchestrator.py
├── tests/
└── demo.py
```

---

## 🐛 Troubleshooting

### Cannot Import 'src'

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
```bash
# Make sure you're in phase1 directory!
cd d:\github\Hackathon-II-Claude-Code-Spec-Driven-Development\phase1

# Verify you're in the right place
pwd  # Should show: .../phase1

# Then run commands
python -m src.agent.tui
```

### Using Launcher Scripts

**Windows PowerShell:**
```powershell
# From root directory
.\launch-tui.ps1
```

**Linux/Mac Bash:**
```bash
# From root directory
chmod +x launch-tui.sh
./launch-tui.sh
```

---

## 📚 Full Documentation

For complete documentation with all examples, see:
- [Detailed Guide](./constitution/CONSTITUTION.md)
- [Specifications](./spec/phase-1-spec.md)
- [Subagent Definitions](./.specify/subagents/)

---

## 🎯 Quick Reference Card

```bash
# IMPORTANT: Run from phase1 directory
cd phase1

# Interactive TUI
python -m src.agent.tui

# Add task
python -m src.todo.cli add "Task" --priority high

# List tasks
python -m src.todo.cli list

# Generate K8s
python -c "from src.agent.advanced_agents import CloudArchitectAgent; print(CloudArchitectAgent().run('k8s app nginx:latest'))"

# Run tests
pytest -q

# Demo
python demo.py
```

---

**Built with ❤️ using Claude Code, MCP, Rich, Python 3.11+**  
**Featuring: Kubernetes • Docker • Terraform • GitHub Actions • MCP • Reusable Intelligence**

🚀 **Production-ready AI-powered todo app!**
