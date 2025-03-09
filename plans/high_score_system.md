# High Score System Implementation Plan

## Overview
Implement a persistent high score system that stores the top 10 scores with player names and dates. Display these scores in a modal when the player dies, with options to retry or quit.

## Technical Specifications

### Data Structure

```json
{
  "high_scores": [
    {
      "player_name": "string (max 20 chars)",
      "score": "integer",
      "date": "ISO format datetime string"
    }
  ]
}
```

### Components

1. **HighScoreManager (high_scores.py)**
   - Manages persistent storage of scores
   - Validates and sorts high scores
   - Handles file I/O operations
   ```python
   MAX_SCORES = 10
   MAX_NAME_LENGTH = 20
   SAVE_FILE_PATH = "data/high_scores.json"
   ```

2. **GameOverModal (game_over_modal.py)**
   - Displays high scores overlay
   - Handles player name input
   - Provides retry/quit options
   ```python
   MODAL_BG_COLOR = (0, 0, 0, 128)  # Semi-transparent black
   MODAL_WIDTH = 600
   MODAL_HEIGHT = 400
   ```

## Implementation Steps

### 1. File System Setup
```
src/
├── high_scores.py
├── game_over_modal.py
└── data/
    └── high_scores.json
```

### 2. High Score Manager Implementation
- Create HighScoreManager class
- Implement file operations (read/write)
- Add score validation and sorting
- Handle file creation if not exists

### 3. Game Over Modal Implementation
- Create GameOverModal class
- Implement modal rendering
- Add text input for player name
- Create retry/quit buttons
- Handle keyboard/mouse input

### 4. Main Game Integration
- Add game over state handling
- Integrate modal display
- Connect high score system
- Implement retry functionality

## User Interface Flow

1. **Player Dies**
   - Game detects player death
   - Loads high scores
   - Shows modal with scores

2. **High Score Modal**
   - Shows current score
   - Displays top 10 high scores with:
     * Player name
     * Score
     * Date
   - Provides input field if new high score
   - Shows retry and quit buttons

3. **Button Actions**
   - Retry: Reset game state and restart
   - Quit: Exit to main menu/close game

## Testing Criteria

1. **High Score Storage**
   - Verify persistence between game sessions
   - Check max scores limit (10)
   - Validate player name length (max 20)
   - Test score sorting

2. **Modal Display**
   - Test visibility and positioning
   - Verify text input functionality
   - Check button interactions
   - Validate display formatting

3. **Game Integration**
   - Test death detection
   - Verify score recording
   - Check retry functionality
   - Validate quit operation

## Dependencies
- Pygame (UI rendering)
- JSON (data storage)
- datetime (timestamp recording)
