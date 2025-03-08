# Python Type Hints Guidelines

## Core Rules
- Use built-in types over typing module types
- Add type hints to all function parameters and return values
- Use Protocol for interfaces

## Built-in Types
```python
# ✅ Use these
def process(
    data: dict[str, int],
    flags: tuple[bool, ...],
    items: list[str]
) -> set[int]: ...

# ❌ Avoid these
from typing import Dict, Tuple, List, Set
def process(
    data: Dict[str, int],
    flags: Tuple[bool, ...],
    items: List[str]
) -> Set[int]: ...
```

## Protocol Usage
```python
from typing import Protocol

# Define interface
class DataStoreProtocol(Protocol):
    def save(self, key: str, value: bytes) -> bool: ...
    def load(self, key: str) -> bytes: ...

# Use interface
def process_data(store: DataStoreProtocol, key: str) -> bytes:
    if store.save(key, b"data"):
        return store.load(key)
    raise ValueError("Save failed")
```

## Type Variables
```python
from typing import TypeVar

T = TypeVar('T')
def first(items: list[T]) -> T:
    return items[0]
```

## Optional and Union
```python
# Python 3.10+
def get_user(id: str) -> User | None: ...

# Earlier versions
from typing import Optional
def get_user(id: str) -> Optional[User]: ...
```

See clean_architecture.md for more Protocol examples in clean architecture context.
