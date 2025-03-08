# Dependency Injection Guidelines

## Core Principles
- Pass dependencies through constructors
- Use Protocol interfaces
- Depend on abstractions

## Basic Pattern
```python
from typing import Protocol

# Interface
class LoggerProtocol(Protocol):
    def log(self, message: str) -> None: ...

# Service depending on interface
class UserService:
    def __init__(self, logger: LoggerProtocol) -> None:
        self.logger = logger

    def create_user(self, name: str) -> None:
        self.logger.log(f"Creating user: {name}")
```

## Container Pattern
```python
class Container:
    def __init__(self) -> None:
        self._services: dict[type, object] = {}

    def register(self, interface: type, implementation: object) -> None:
        self._services[interface] = implementation

    def resolve(self, interface: type) -> object:
        return self._services[interface]

# Usage
container = Container()
container.register(LoggerProtocol, FileLogger())
service = UserService(container.resolve(LoggerProtocol))
```

## Factory Pattern
```python
class UserRepositoryFactory(Protocol):
    def create(self) -> UserRepositoryProtocol: ...

class SQLiteRepositoryFactory:
    def create(self) -> UserRepositoryProtocol:
        return SQLiteUserRepository()

# Usage
def create_usecase(factory: UserRepositoryFactory) -> CreateUserUseCase:
    return CreateUserUseCase(factory.create())
```

## Testing with DI
```python
class MockLogger:
    def __init__(self) -> None:
        self.logs: list[str] = []

    def log(self, message: str) -> None:
        self.logs.append(message)

def test_user_service():
    logger = MockLogger()
    service = UserService(logger)
    service.create_user("test")
    assert "Creating user: test" in logger.logs
```

## Best Practices
1. Keep interfaces small
2. Use Protocol for type safety
3. Inject all dependencies
4. Use factories for complex creation
5. Consider using DI container for large apps
