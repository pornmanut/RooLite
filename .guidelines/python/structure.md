# Python Guidelines Structure

## Quick Access Guide
1. Starting a project:
   - `clean_architecture.md` - Project structure
   - `venv.md` - Environment setup
   - `formatting.md` - Code style

2. Development:
   - `typing.md` - Type hints and Protocol
   - `dependency_injection.md` - DI patterns
   - `logging.md` - Logging setup

3. Testing:
   - `testing.md` - Test organization
   - `workflow.md` - Development process

4. Complete Example:
   - `example.md` - All guidelines integrated

## Guidelines Overview
Each file is self-contained and optimized for token usage:

1. `venv.md` - Virtual environment (smallest, load first)
2. `formatting.md` - Black and isort setup
3. `typing.md` - Type hints with Protocol
4. `logging.md` - Logging configuration
5. `testing.md` - pytest guidelines
6. `clean_architecture.md` - Project structure
7. `dependency_injection.md` - DI patterns
8. `workflow.md` - Development process
9. `example.md` - Practical implementation

## Usage in Different Modes

### Architect Mode
```python
# Load structure first
<read_file>
<path>.guidelines/python/structure.md</path>
</read_file>

# Then load specific guidelines
<read_file>
<path>.guidelines/python/[needed_guideline].md</path>
</read_file>
```

### Code Mode
1. Reference structure.md first
2. Load only needed guidelines
3. Use example.md for patterns

## Dependencies Between Guidelines
- clean_architecture.md → typing.md, dependency_injection.md
- testing.md → typing.md (for mocks)
- example.md → all guidelines

## Token Optimization
- Each file is independent
- Load only what you need
- Examples are minimal but complete
- Reference other files instead of duplicating
