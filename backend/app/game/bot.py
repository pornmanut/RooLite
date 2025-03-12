from typing import Tuple, Optional
from .models import GameState, Player, Move

class TicTacToeBot:
    def __init__(self, max_depth: int = 9):
        self.max_depth = max_depth

    def get_best_move(self, game_state: GameState) -> Optional[Move]:
        """Find the best move for the AI using minimax algorithm."""
        best_score = float('-inf')
        best_move = None

        for row, col in game_state.get_empty_cells():
            # Try the move
            game_state.board[row][col] = Player.AI
            
            # Calculate score for this move
            score = self._minimax(game_state, 0, False)
            
            # Undo the move
            game_state.board[row][col] = Player.EMPTY

            # Update best move if this score is better
            if score > best_score:
                best_score = score
                best_move = Move(row=row, col=col)

        return best_move

    def _minimax(self, game_state: GameState, depth: int, is_maximizing: bool) -> float:
        """
        Implements the minimax algorithm to find the best move.
        
        Args:
            game_state: Current state of the game
            depth: Current depth in the game tree
            is_maximizing: True if it's AI's turn, False for human's turn
        
        Returns:
            float: The score for the current board state
        """
        # Check for terminal states
        winner = game_state.check_winner()
        if winner == Player.AI:
            return 10 - depth
        if winner == Player.HUMAN:
            return -10 + depth
        if not game_state.get_empty_cells() or depth == self.max_depth:
            return 0

        if is_maximizing:
            # AI's turn - maximize score
            best_score = float('-inf')
            for row, col in game_state.get_empty_cells():
                game_state.board[row][col] = Player.AI
                score = self._minimax(game_state, depth + 1, False)
                game_state.board[row][col] = Player.EMPTY
                best_score = max(score, best_score)
            return best_score
        else:
            # Human's turn - minimize score
            best_score = float('inf')
            for row, col in game_state.get_empty_cells():
                game_state.board[row][col] = Player.HUMAN
                score = self._minimax(game_state, depth + 1, True)
                game_state.board[row][col] = Player.EMPTY
                best_score = min(score, best_score)
            return best_score
