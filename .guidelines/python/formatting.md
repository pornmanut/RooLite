# Python Formatting Guidelines

## Black Usage
```bash
pip install black
```

### Configuration
- Use default settings
- No custom configurations needed
- Line length: 88 characters (default)

### Running
```bash
black .
```

## Import Sorting
```bash
pip install isort
```

### Configuration
```toml
# pyproject.toml
[tool.isort]
profile = "black"
multi_line_output = 3
```

### Running
```bash
isort .
```

## VSCode Integration
```json
{
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

## Example Formatting
```python
# Black will format this:
def process_data(
    parameter_one: str,
    parameter_two: int,
    parameter_three: dict[str, int],
) -> list[str]:
    return [
        item
        for item in process(parameter_one)
        if validate(item, parameter_two)
    ]
```

## Pre-commit Setup
```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
