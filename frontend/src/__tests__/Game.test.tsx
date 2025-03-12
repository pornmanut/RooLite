import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Game } from '@/components/Game';
import gameService from '@/services/gameService';

// Mock the game service
jest.mock('@/services/gameService');
const mockedGameService = gameService as jest.Mocked<typeof gameService>;

describe('Game Component', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    
    // Mock the initial game state
    mockedGameService.createGame.mockResolvedValue({
      game_id: 1,
      state: {
        board: [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        current_player: 'X',
        status: 'IN_PROGRESS'
      }
    });
  });

  test('renders the game board', async () => {
    render(<Game />);
    
    // Wait for the game to load
    await waitFor(() => {
      expect(screen.getByText(/Current player: Your turn/i)).toBeInTheDocument();
    });

    // Should have 9 cells
    const cells = screen.getAllByRole('button');
    expect(cells.length).toBe(10); // 9 game cells + 1 "New Game" button
  });

  test('handles player moves', async () => {
    // Mock the move response
    mockedGameService.makeMove.mockResolvedValue({
      state: {
        board: [['X', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']],
        current_player: 'X',
        status: 'IN_PROGRESS'
      }
    });

    render(<Game />);

    // Wait for the game to load
    await waitFor(() => {
      expect(screen.getByText(/Current player: Your turn/i)).toBeInTheDocument();
    });

    // Click the first cell
    const cells = screen.getAllByRole('button');
    fireEvent.click(cells[0]);

    // Wait for the move to be processed
    await waitFor(() => {
      expect(mockedGameService.makeMove).toHaveBeenCalledWith(1, { row: 0, col: 0 });
    });
  });

  test('handles game completion', async () => {
    // Mock a winning game state
    mockedGameService.makeMove.mockResolvedValue({
      state: {
        board: [['X', 'X', 'X'], ['O', 'O', ' '], [' ', ' ', ' ']],
        current_player: 'X',
        status: 'PLAYER_WIN'
      }
    });

    render(<Game />);

    // Wait for the game to load
    await waitFor(() => {
      expect(screen.getByText(/Current player: Your turn/i)).toBeInTheDocument();
    });

    // Click a cell to win
    const cells = screen.getAllByRole('button');
    fireEvent.click(cells[2]);

    // Wait for the winning message
    await waitFor(() => {
      expect(screen.getByText(/Congratulations! You won!/i)).toBeInTheDocument();
    });
  });

  test('starts new game', async () => {
    render(<Game />);

    // Wait for the game to load
    await waitFor(() => {
      expect(screen.getByText(/Current player: Your turn/i)).toBeInTheDocument();
    });

    // Click the "New Game" button
    const newGameButton = screen.getByText(/New Game/i);
    fireEvent.click(newGameButton);

    // Verify that createGame was called again
    await waitFor(() => {
      expect(mockedGameService.createGame).toHaveBeenCalledTimes(2);
    });
  });
});
