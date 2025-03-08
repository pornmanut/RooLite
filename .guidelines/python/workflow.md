# Python Development Workflow

## Setup Steps
1. Create and activate venv (see venv.md)
2. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

## Development Cycle
1. **Start Feature**
   - Create feature branch
   - Plan interfaces using Protocol
   - Write tests first

2. **Implementation Order**
   ```
   Domain -> Repository/Service -> Usecase -> Presentation
   ```
   - Start with domain entities and interfaces
   - Implement repositories/services
   - Create use cases
   - Add presentation layer

3. **Testing Approach**
   - Unit tests alongside code
   - Integration tests in tests/
   - Run tests frequently

4. **Code Quality**
   ```bash
   # Before commit
   black .
   isort .
   pytest
   ```

## Implementation Flow Example
1. Define interface:
```python
class UserStoreProtocol(Protocol):
    def save(self, user: User) -> None: ...
```

2. Write test:
```python
def test_user_creation():
    store = MockUserStore()
    usecase = CreateUser(store)
    user = usecase.execute({"name": "Test"})
    assert store.get(user.id).name == "Test"
```

3. Implement feature:
```python
class CreateUser:
    def __init__(self, store: UserStoreProtocol) -> None:
        self.store = store

    def execute(self, data: dict) -> User:
        user = User(**data)
        self.store.save(user)
        return user
```

## Review Checklist
- [ ] Tests written and passing
- [ ] Type hints added
- [ ] Proper logging
- [ ] Clean architecture followed
- [ ] Code formatted
- [ ] Docstrings added
