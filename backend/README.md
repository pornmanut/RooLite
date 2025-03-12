# Tic-tac-toe Game Backend

A FastAPI-based backend for the Tic-tac-toe game with AI opponent.

## Features

- RESTful API endpoints for game management
- AI opponent using minimax algorithm
- In-memory game state management
- Comprehensive test coverage

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

After starting the server, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

- `POST /game/new` - Create a new game
- `POST /game/{game_id}/move` - Make a move
- `GET /game/{game_id}` - Get game state

## Running Tests

Execute the test suite:
```bash
pytest
```

## Development

The project structure:
```
app/
├── game/
│   ├── __init__.py
│   ├── models.py     # Game state and data models
│   ├── bot.py        # AI opponent implementation
│   └── routes.py     # API endpoints
├── __init__.py
└── main.py          # FastAPI application setup
