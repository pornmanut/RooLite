# Python Testing Guidelines

## Test Organization
1. Unit Tests
   - Place alongside source code
   - Name pattern: `{module}_test.py`
   - Test single module functionality
   ```python
   # src/project_name/core/models.py
   class User:
       def __init__(self, name: str) -> None:
           self.name = name

   # src/project_name/core/models_test.py
   def test_user_creation():
       user = User("test")
       assert user.name == "test"
   ```

2. Integration Tests
   - Place in `tests/integration/`
   - Test multiple module interactions
   - Name pattern: `test_{feature}.py`

## Using pytest.parametrize
```python
import pytest
from unittest import mock

@pytest.mark.parametrize("input_value,expected", [
    ({"key": 1}, True),     # success case
    ({}, False),            # empty dict case
    (None, False),          # edge case - None
    ({"wrong": 1}, False)   # failure case
])
def test_validation(input_value, expected):
    """Parametrized test with multiple cases."""
    assert validate_data(input_value) == expected
```

## Mocking Example
```python
from unittest import mock

@mock.patch('module.external_service')
def test_service_call(mock_service):
    # Configure mock
    mock_service.return_value = {'status': 'success'}
    
    # Test execution
    result = your_function()
    
    # Verify mock was called correctly
    mock_service.assert_called_once()
```

## Test Categories to Include
1. Success Cases
   - Valid inputs
   - Expected workflow paths
   - Boundary conditions

2. Failure Cases
   - Invalid inputs
   - Error conditions
   - Exception handling

3. Edge Cases
   - Empty inputs
   - None values
   - Boundary values
   - Maximum/minimum values

## Best Practices
1. Unit Tests:
   - Keep close to source code
   - Quick to run
   - No external dependencies
   - One module per test file

2. Integration Tests:
   - Test module interactions
   - May require setup/teardown
   - Can use external resources
   - Test complete features

3. Test isolation:
   - Each test should be independent
   - Use fixtures for setup/teardown
   - Reset mocks between tests

4. Assertion best practices:
   - One primary assertion per test
   - Use descriptive assertion messages
   - Test one behavior at a time

## Running Tests
```bash
# Run all tests (both unit and integration)
pytest

# Run only unit tests in a specific module
pytest src/project_name/core/models_test.py

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=src
