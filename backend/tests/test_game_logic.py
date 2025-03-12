import pytest
from app.game.models import GameState, Move, Player, GameStatus
from app.game.bot import TicTacToeBot

def test_new_game_creation():
    game = GameState.new_game()
    assert game.current_player == Player.HUMAN
    assert game.status == GameStatus.IN_PROGRESS
    assert len(game.board) == 3
    assert all(len(row) == 3 for row in game.board)
    assert all(cell == Player.EMPTY for row in game.board for cell in row)

def test_valid_move():
    game = GameState.new_game()
    move = Move(row=0, col=0)
    assert game.is_valid_move(move) == True
    assert game.make_move(move, Player.HUMAN) == True
    assert game.board[0][0] == Player.HUMAN

def test_invalid_move():
    game = GameState.new_game()
    # Make initial move
    first_move = Move(row=0, col=0)
    game.make_move(first_move, Player.HUMAN)
    
    # Try to move in the same position
    second_move = Move(row=0, col=0)
    assert game.is_valid_move(second_move) == False
    assert game.make_move(second_move, Player.AI) == False

def test_win_detection_horizontal():
    game = GameState.new_game()
    # Create a winning horizontal line for HUMAN
    moves = [
        Move(row=0, col=0),
        Move(row=0, col=1),
        Move(row=0, col=2)
    ]
    for move in moves:
        game.make_move(move, Player.HUMAN)
    
    game.update_game_status()
    assert game.status == GameStatus.PLAYER_WIN

def test_win_detection_vertical():
    game = GameState.new_game()
    # Create a winning vertical line for HUMAN
    moves = [
        Move(row=0, col=0),
        Move(row=1, col=0),
        Move(row=2, col=0)
    ]
    for move in moves:
        game.make_move(move, Player.HUMAN)
    
    game.update_game_status()
    assert game.status == GameStatus.PLAYER_WIN

def test_win_detection_diagonal():
    game = GameState.new_game()
    # Create a winning diagonal line for HUMAN
    moves = [
        Move(row=0, col=0),
        Move(row=1, col=1),
        Move(row=2, col=2)
    ]
    for move in moves:
        game.make_move(move, Player.HUMAN)
    
    game.update_game_status()
    assert game.status == GameStatus.PLAYER_WIN

def test_draw_detection():
    game = GameState.new_game()
    # Create a draw scenario
    moves = [
        (0, 0, Player.HUMAN), (0, 1, Player.AI), (0, 2, Player.HUMAN),
        (1, 0, Player.AI), (1, 1, Player.HUMAN), (1, 2, Player.AI),
        (2, 0, Player.AI), (2, 1, Player.HUMAN), (2, 2, Player.AI)
    ]
    for row, col, player in moves:
        game.make_move(Move(row=row, col=col), player)
    
    game.update_game_status()
    assert game.status == GameStatus.DRAW

def test_bot_makes_winning_move():
    game = GameState.new_game()
    bot = TicTacToeBot()
    
    # Set up a board where bot can win in one move
    # O O -
    # X X -
    # - - -
    game.make_move(Move(row=0, col=0), Player.AI)
    game.make_move(Move(row=0, col=1), Player.AI)
    game.make_move(Move(row=1, col=0), Player.HUMAN)
    game.make_move(Move(row=1, col=1), Player.HUMAN)
    
    # Bot should choose (0, 2) to win
    best_move = bot.get_best_move(game)
    assert best_move is not None
    assert best_move.row == 0
    assert best_move.col == 2
