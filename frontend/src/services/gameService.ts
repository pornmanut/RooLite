import axios from 'axios';
import { GameResponse, Move, MoveResponse } from '@/types/game';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: 'http://localhost:8000',  // Direct backend URL
    headers: {
        'Content-Type': 'application/json',
    },
});

const gameService = {
    /**
     * Create a new game
     */
    createGame: async (): Promise<GameResponse> => {
        const response = await api.post<GameResponse>('/game/new');
        return response.data;
    },

    /**
     * Make a move in the game
     */
    makeMove: async (gameId: number, move: Move): Promise<MoveResponse> => {
        const response = await api.post<MoveResponse>(
            `/game/${gameId}/move`,
            move
        );
        return response.data;
    },

    /**
     * Get the current game state
     */
    getGameState: async (gameId: number): Promise<MoveResponse> => {
        const response = await api.get<MoveResponse>(`/game/${gameId}`);
        return response.data;
    },
};

export default gameService;
