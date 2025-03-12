import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Tic-tac-toe API is running"
    }

def test_create_new_game():
    """Test creating a new game"""
    response = client.post("/game/new")
    assert response.status_code == 200
    data = response.json()
    
    assert "game_id" in data
    assert "state" in data
    assert data["state"]["status"] == "IN_PROGRESS"
    assert len(data["state"]["board"]) == 3
    assert all(len(row) == 3 for row in data["state"]["board"])

def test_make_valid_move():
    """Test making a valid move"""
    # Create a new game
    new_game = client.post("/game/new").json()
    game_id = new_game["game_id"]
    
    # Make a move
    move = {"row": 0, "col": 0}
    response = client.post(f"/game/{game_id}/move", json=move)
    assert response.status_code == 200
    
    data = response.json()
    assert "state" in data
    assert data["state"]["board"][0][0] == "X"  # Player's move
    assert data["state"]["status"] in ["IN_PROGRESS", "PLAYER_WIN", "AI_WIN", "DRAW"]

def test_make_invalid_move():
    """Test making an invalid move"""
    # Create a new game
    new_game = client.post("/game/new").json()
    game_id = new_game["game_id"]
    
    # Make initial move
    first_move = {"row": 0, "col": 0}
    client.post(f"/game/{game_id}/move", json=first_move)
    
    # Try to move in the same position
    second_move = {"row": 0, "col": 0}
    response = client.post(f"/game/{game_id}/move", json=second_move)
    assert response.status_code == 400

def test_get_game_state():
    """Test getting the state of an existing game"""
    # Create a new game
    new_game = client.post("/game/new").json()
    game_id = new_game["game_id"]
    
    # Get game state
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert "state" in data

def test_get_nonexistent_game():
    """Test getting the state of a non-existent game"""
    response = client.get("/game/999")
    assert response.status_code == 404

def test_complete_game_flow():
    """Test a complete game flow"""
    # Create new game
    new_game = client.post("/game/new").json()
    game_id = new_game["game_id"]
    
    # Make moves until game is complete
    moves = [
        (0, 0), (0, 1), (0, 2),  # Top row
    ]
    
    for row, col in moves:
        response = client.post(f"/game/{game_id}/move", json={"row": row, "col": col})
        assert response.status_code == 200
        
        state = response.json()["state"]
        if state["status"] != "IN_PROGRESS":
            # Game is finished
            assert state["status"] in ["PLAYER_WIN", "AI_WIN", "DRAW"]
            break
