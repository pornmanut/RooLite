# Python Logging Guidelines

## Basic Setup
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

## Log Levels
- DEBUG: Development details
  ```python
  logger.debug(f"Processing item: {item_id}")
  ```
- INFO: Normal operations
  ```python
  logger.info("Operation completed")
  ```
- WARNING: Handled issues
  ```python
  logger.warning("Feature deprecated")
  ```
- ERROR: Need attention
  ```python
  logger.error(f"Failed: {str(e)}", exc_info=True)
  ```
- CRITICAL: System failures
  ```python
  logger.critical("Database connection lost")
  ```

## Best Practices
1. Use structured logging
```python
# ✅ Good
logger.info("User %s logged in", username)

# ❌ Avoid
logger.info(f"User {username} logged in")
```

2. Include context
```python
logger.error("Failed", extra={"op": op_id, "user": user_id})
```

3. Use exception logging
```python
try:
    process()
except Exception:
    logger.exception("Failed")  # Includes traceback
```

4. Get logger per module
```python
logger = logging.getLogger(__name__)
