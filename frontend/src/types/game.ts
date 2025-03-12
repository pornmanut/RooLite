export type Player = 'X' | 'O' | ' ';
export type Board = Player[][];

export type GameStatus = 'IN_PROGRESS' | 'PLAYER_WIN' | 'AI_WIN' | 'DRAW';

export interface GameState {
    board: Board;
    current_player: Player;
    status: GameStatus;
}

export interface Move {
    row: number;
    col: number;
}

export interface GameResponse {
    game_id: number;
    state: GameState;
}

export interface MoveResponse {
    state: GameState;
}
