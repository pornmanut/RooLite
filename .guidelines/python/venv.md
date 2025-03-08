# Python Virtual Environment Guidelines

## Setup
```bash
# Create
python -m venv .venv

# Activate
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Key Rules
1. Always use venv for projects
2. Never install globally
3. Add `.venv` to `.gitignore`

## Dependencies
```bash
# Save project dependencies
pip freeze > requirements.txt

# Development dependencies
pip freeze > requirements-dev.txt
```

## VS Code Setup
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

## Verification
```bash
# Check active Python
which python  # Unix
where python  # Windows

# Should point to .venv
```

## Best Practices
1. One venv per project
2. Update requirements.txt when adding packages
3. Separate dev dependencies
4. Check venv is active before running/testing
