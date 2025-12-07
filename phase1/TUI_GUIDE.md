# Enhanced TUI Quick Start Guide

## 🚀 Launch the TUI

```bash
cd phase1
python -m src.agent.tui
```

## ✨ What's New in Enhanced TUI?

### 🎯 Super Easy Commands
- **Natural language** - Just type like you're talking
- **No complex syntax** - No need for function calls
- **Instant help** - Type 'help' anytime
- **Clear feedback** - Beautiful formatted responses

### 📝 Simple Command Examples

```
# Add a task (SO EASY!)
add Buy groceries

# Another task
add Call dentist tomorrow

# List all tasks
list

# Search for tasks
search grocery

# View stats
stats

# Complete a task (use ID from list)
complete a1b2c3

# Delete a task
delete a1b2c3

# Get help
help

# Clear screen
clear

# Exit
exit
```

### 🎨 Beautiful Features

1. **Welcome Screen** - Clear instructions when you start
2. **Color-Coded Output**:
   - 🟢 Green = Success
   - 🔴 Red = Errors
   - 🟡 Yellow = Warnings
   - 🔵 Blue = Info
3. **Formatted Panels** - Tasks, stats, and details in nice boxes
4. **Help System** - Complete command reference
5. **Smart Responses** - Different formatting for different commands

## 🎯 All Commands

| Command | What It Does | Example |
|---------|-------------|---------|
| `add <task>` | Add new task | `add Buy milk` |
| `list` | Show all tasks | `list` |
| `list pending` | Show pending only | `list pending` |
| `list completed` | Show done tasks | `list completed` |
| `search <word>` | Find tasks | `search milk` |
| `complete <id>` | Mark as done | `complete a1b2` |
| `delete <id>` | Remove task | `delete a1b2` |
| `details <id>` | Full task info | `details a1b2` |
| `stats` | View statistics | `stats` |
| `help` | Show all commands | `help` |
| `clear` | Clear screen | `clear` |
| `exit` | Quit TUI | `exit` |

## 💡 Pro Tips

1. **Task IDs**: When you run `list`, you'll see short IDs (like `a1b2c3`)
   - Use these for `complete`, `delete`, and `details` commands

2. **Natural Commands**: The TUI understands natural language:
   - `add Buy groceries` ✅
   - `search milk` ✅
   - `stats` ✅

3. **Quick Exit**: Press Ctrl+C or type `exit`

4. **Help Anytime**: Forgot a command? Just type `help`

## 🐛 Troubleshooting

### TUI Won't Start?
```bash
# Make sure you're in phase1 directory!
cd d:\github\Hackathon-II-Claude-Code-Spec-Driven-Development\phase1

# Then run
python -m src.agent.tui
```

### Module Not Found?
```bash
# Install dependencies
pip install -r requirements.txt
```

## 🎉 Try It Now!

```bash
cd phase1
python -m src.agent.tui

# Then type:
add Buy groceries
list
stats
help
exit
```

**Enjoy your enhanced, professional TUI!** 🚀
