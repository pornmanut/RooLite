from enum import Enum
from typing import List, Optional, Tuple
from pydantic import BaseModel

class Player(str, Enum):
    HUMAN = "X"
    AI = "O"
    EMPTY = " "

class GameStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    PLAYER_WIN = "PLAYER_WIN"
    AI_WIN = "AI_WIN"
    DRAW = "DRAW"

class Move(BaseModel):
    row: int
    col: int

class GameState(BaseModel):
    board: List[List[str]]
    current_player: Player
    status: GameStatus

    @classmethod
    def new_game(cls) -> "GameState":
        """Create a new game with an empty board."""
        return cls(
            board=[[Player.EMPTY for _ in range(3)] for _ in range(3)],
            current_player=Player.HUMAN,
            status=GameStatus.IN_PROGRESS
        )

    def is_valid_move(self, move: Move) -> bool:
        """Check if a move is valid."""
        return (
            0 <= move.row < 3 and
            0 <= move.col < 3 and
            self.board[move.row][move.col] == Player.EMPTY
        )

    def make_move(self, move: Move, player: Player) -> bool:
        """Attempt to make a move on the board."""
        if not self.is_valid_move(move):
            return False
        
        self.board[move.row][move.col] = player
        return True

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get all empty cells on the board."""
        return [
            (row, col)
            for row in range(3)
            for col in range(3)
            if self.board[row][col] == Player.EMPTY
        ]

    def check_winner(self) -> Optional[Player]:
        """Check if there's a winner."""
        # Check rows, columns and diagonals
        for i in range(3):
            # Check rows
            if (self.board[i][0] != Player.EMPTY and 
                self.board[i][0] == self.board[i][1] == self.board[i][2]):
                return Player(self.board[i][0])
            
            # Check columns
            if (self.board[0][i] != Player.EMPTY and
                self.board[0][i] == self.board[1][i] == self.board[2][i]):
                return Player(self.board[0][i])

        # Check diagonals
        if (self.board[0][0] != Player.EMPTY and
            self.board[0][0] == self.board[1][1] == self.board[2][2]):
            return Player(self.board[0][0])
        
        if (self.board[0][2] != Player.EMPTY and
            self.board[0][2] == self.board[1][1] == self.board[2][0]):
            return Player(self.board[0][2])

        return None

    def update_game_status(self) -> None:
        """Update the game status based on the current board state."""
        winner = self.check_winner()
        if winner:
            self.status = (
                GameStatus.PLAYER_WIN if winner == Player.HUMAN
                else GameStatus.AI_WIN
            )
        elif not self.get_empty_cells():
            self.status = GameStatus.DRAW
        else:
            self.status = GameStatus.IN_PROGRESS
