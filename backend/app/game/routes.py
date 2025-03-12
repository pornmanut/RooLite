from fastapi import APIRouter, HTTPException
from .models import GameState, Move, Player, GameStatus
from .bot import TicTacToeBot

router = APIRouter()
bot = TicTacToeBot()

# Store active games in memory (in production, use a proper database)
games = {}

@router.post("/new")
async def create_game() -> dict:
    """Create a new game and return its initial state."""
    game_state = GameState.new_game()
    game_id = len(games)  # Simple counter for game IDs
    games[game_id] = game_state
    
    return {
        "game_id": game_id,
        "state": game_state
    }

@router.post("/{game_id}/move")
async def make_move(game_id: int, move: Move) -> dict:
    """Process a player's move and return the updated game state."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_state = games[game_id]
    
    # Check if game is already over
    if game_state.status != GameStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Game is already over")
    
    # Process player's move
    if not game_state.make_move(move, Player.HUMAN):
        raise HTTPException(status_code=400, detail="Invalid move")
    
    # Update game status after player's move
    game_state.update_game_status()
    
    # If game is not over, let AI make its move
    if game_state.status == GameStatus.IN_PROGRESS:
        ai_move = bot.get_best_move(game_state)
        if ai_move:
            game_state.make_move(ai_move, Player.AI)
            game_state.update_game_status()
    
    return {
        "state": game_state
    }

@router.get("/{game_id}")
async def get_game_state(game_id: int) -> dict:
    """Get the current state of a game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return {
        "state": games[game_id]
    }
