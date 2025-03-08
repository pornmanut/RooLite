# Clean Architecture Guidelines

## Directory Layout
```
project_name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── domain/           # Enterprise business rules
│       │   ├── __init__.py
│       │   ├── entities/     # Enterprise business entities
│       │   │   ├── __init__.py
│       │   │   ├── user.py
│       │   │   └── user_test.py
│       │   └── repositories/ # Abstract repository interfaces
│       │       ├── __init__.py
│       │       ├── user_repository.py
│       │       └── user_repository_test.py
│       ├── usecase/         # Application business rules
│       │   ├── __init__.py
│       │   ├── user/
│       │   │   ├── __init__.py
│       │   │   ├── create_user.py
│       │   │   └── create_user_test.py
│       │   └── auth/
│       │       ├── __init__.py
│       │       ├── login.py
│       │       └── login_test.py
│       ├── repository/      # Repository implementations
│       │   ├── __init__.py
│       │   ├── sqlite/
│       │   │   ├── __init__.py
│       │   │   ├── user_repository.py
│       │   │   └── user_repository_test.py
│       │   └── mongo/
│       │       ├── __init__.py
│       │       ├── user_repository.py
│       │       └── user_repository_test.py
│       ├── service/         # External services integration
│       │   ├── __init__.py
│       │   ├── email/
│       │   │   ├── __init__.py
│       │   │   ├── sender.py
│       │   │   └── sender_test.py
│       │   └── storage/
│       │       ├── __init__.py
│       │       ├── s3.py
│       │       └── s3_test.py
│       └── presentation/    # User interface adapters
│           ├── __init__.py
│           ├── cli/        # Command-line interface
│           │   ├── __init__.py
│           │   ├── commands.py
│           │   └── commands_test.py
│           └── api/        # REST API interface
│               ├── __init__.py
│               ├── routes.py
│               └── routes_test.py
```

## Layer Dependencies
```
presentation -> usecase -> domain <- repository <- service
```

## Interface Definition with Protocol
```python
# domain/repositories/user_repository.py
from typing import Protocol
from domain.entities.user import User

class UserRepositoryProtocol(Protocol):
    """Interface for user storage operations."""
    def save(self, user: User) -> None: ...
    def get(self, id: str) -> User: ...
    def delete(self, id: str) -> None: ...

# domain/services/email_service.py
class EmailServiceProtocol(Protocol):
    """Interface for email operations."""
    def send(self, to: str, subject: str, body: str) -> bool: ...
    def send_bulk(self, emails: list[tuple[str, str, str]]) -> dict[str, bool]: ...
```

## Layer Responsibilities
1. **Domain Layer** (`domain/`)
   - Core business entities
   - Repository interfaces using Protocol
   - Pure business logic
   - No external dependencies

2. **Usecase Layer** (`usecase/`)
   - Application-specific business rules
   - Orchestrates entities
   - Depends only on domain layer interfaces
   ```python
   class CreateUserUseCase:
       def __init__(
           self,
           repo: UserRepositoryProtocol,
           email: EmailServiceProtocol
       ) -> None:
           self.repo = repo
           self.email = email
   ```

3. **Repository Layer** (`repository/`)
   - Implements domain repository interfaces
   - Handles data persistence
   - Multiple implementations possible
   ```python
   class SQLiteUserRepository:
       """Implements UserRepositoryProtocol."""
       def save(self, user: User) -> None: ...
       def get(self, id: str) -> User: ...
   ```

4. **Service Layer** (`service/`)
   - External service integrations
   - Implements service interfaces
   - Infrastructure concerns

5. **Presentation Layer** (`presentation/`)
   - User interface adapters (CLI, API)
   - Depends on usecase layer
   - Handles I/O and formatting

## Best Practices
1. Use Protocol for interfaces
   - Clear contracts
   - Type safety
   - Easy testing

2. Dependency Injection
   - Pass dependencies through constructors
   - Use interfaces, not concrete implementations
   - Makes testing easier

3. Layer Isolation
   - Each layer has clear responsibilities
   - Dependencies flow inward
   - Use interfaces for communication

4. Testing
   - Unit tests alongside implementation
   - Mock interfaces for isolation
   - Integration tests in `tests/` directory

## Example Implementation
```python
# Domain Entity
class User:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

# Repository Interface
class UserRepositoryProtocol(Protocol):
    def save(self, user: User) -> None: ...
    def get(self, id: str) -> User: ...

# Use Case
class CreateUserUseCase:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    def execute(self, user_data: dict) -> User:
        user = User(**user_data)
        self.repo.save(user)
        return user

# Repository Implementation
class SQLiteUserRepository:
    def save(self, user: User) -> None:
        # Implementation
        pass

    def get(self, id: str) -> User:
        # Implementation
        pass

# Presentation
class UserCLI:
    def __init__(self, create_user: CreateUserUseCase) -> None:
        self.create_user = create_user

    def add_user(self, name: str) -> None:
        user = self.create_user.execute({"name": name})
        print(f"Created user: {user.name}")
