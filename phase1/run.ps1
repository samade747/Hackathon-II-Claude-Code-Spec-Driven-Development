# PowerShell script to run the Todo Agent TUI
$ErrorActionPreference = "Stop"

Write-Host "🚀 Launching Evolution of Todo (TUI)..." -ForegroundColor Cyan

# Check for python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found. Please install Python 3.11+."
    exit 1
}

# Install dependencies if needed (simple check)
# In production, check for venv usage
if (!(pip show rich)) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install rich
}

# Run the TUI
$env:PYTHONPATH = "$PWD"
python -m src.agent.tui
