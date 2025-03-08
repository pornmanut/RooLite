# Python Guidelines Example

This example shows how all guidelines integrate in a real project.

## Project Structure
```
myapp/
├── src/
│   └── myapp/
│       ├── domain/
│       │   ├── user.py          # Entity
│       │   └── user_test.py     # Unit test
│       ├── repository/
│       │   ├── interface.py     # Protocol
│       │   └── sqlite.py        # Implementation
│       └── usecase/
│           └── create_user.py   # Business logic
```

## Complete Example
```python
# domain/user.py
class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id: str | None = None

# repository/interface.py
from typing import Protocol
from ..domain.user import User

class UserRepo(Protocol):
    def save(self, user: User) -> None: ...
    def get(self, id: str) -> User: ...

# repository/sqlite.py
import logging
from typing import Any
from .interface import UserRepo
from ..domain.user import User

logger = logging.getLogger(__name__)

class SQLiteRepo:
    def __init__(self, db: Any) -> None:
        self.db = db
        
    def save(self, user: User) -> None:
        logger.info("Saving user: %s", user.name)
        # Implementation...

# usecase/create_user.py
from ..domain.user import User
from ..repository.interface import UserRepo

class CreateUser:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    def execute(self, name: str) -> User:
        user = User(name)
        self.repo.save(user)
        return user

# tests/integration/test_user_flow.py
import pytest
from myapp.domain.user import User
from myapp.usecase.create_user import CreateUser

class MockRepo:
    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self.users[user.id] = user

    def get(self, id: str) -> User:
        return self.users[id]

@pytest.mark.parametrize("name", ["Test", "User"])
def test_create_user(name: str) -> None:
    repo = MockRepo()
    usecase = CreateUser(repo)
    user = usecase.execute(name)
    assert user.name == name
```

This example demonstrates:
- Clean Architecture structure
- Protocol interfaces
- Type hints
- Unit test with mock
- Dependency injection
- Proper logging
- Parametrized testing
