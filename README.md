# Tic-tac-toe Game

A full-stack implementation of the classic Tic-tac-toe game with an AI opponent.

## Features

- Python FastAPI backend with AI opponent
- React TypeScript frontend
- Minimax algorithm for AI moves
- Real-time game state updates
- Animated UI with Framer Motion
- RESTful API communication

## Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── game/        # Game logic and API
│   │   └── main.py      # FastAPI application
│   └── tests/           # Backend tests
└── frontend/            # React frontend
    └── src/
        ├── components/  # React components
        ├── services/    # API services
        └── types/       # TypeScript types
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Setup and Running

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Start development server
npm run start
# or
yarn start
```

The frontend will be available at `http://localhost:3000`

## Playing the Game

1. Open `http://localhost:3000` in your browser
2. The game starts automatically with you as 'X'
3. Click any empty cell to make your move
4. The AI will automatically respond with its move
5. Click "New Game" to start a new game at any time

## API Documentation

Backend API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Backend Tests
```bash
cd backend
pytest
```

## Development

- Backend API endpoints are proxied via Vite's dev server
- Frontend uses TypeScript for type safety
- Both backend and frontend include comprehensive testing

## License

MIT License - feel free to use this project for any purpose

## Acknowledgments

- FastAPI for the efficient Python backend framework
- React team for the fantastic frontend library
- Framer Motion for the smooth animations
