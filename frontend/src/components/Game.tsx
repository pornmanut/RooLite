import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Board from './Board';
import gameService from '@/services/gameService';
import { GameState, Move } from '@/types/game';

const GameContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
`;

const StatusText = styled(motion.h2)`
  color: #2c3e50;
  text-align: center;
`;

const Button = styled(motion.button)`
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;

  &:hover {
    background-color: #3498db;
  }
`;

export const Game: React.FC = () => {
  const [gameId, setGameId] = useState<number | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const startNewGame = async () => {
    setIsLoading(true);
    try {
      const response = await gameService.createGame();
      setGameId(response.game_id);
      setGameState(response.state);
    } catch (error) {
      console.error('Error starting new game:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCellClick = async (row: number, col: number) => {
    if (!gameId || !gameState || gameState.status !== 'IN_PROGRESS') return;

    setIsLoading(true);
    try {
      const move: Move = { row, col };
      const response = await gameService.makeMove(gameId, move);
      setGameState(response.state);
    } catch (error) {
      console.error('Error making move:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusMessage = () => {
    if (!gameState) return 'Start a new game!';
    
    switch (gameState.status) {
      case 'IN_PROGRESS':
        return `Current player: ${gameState.current_player === 'X' ? 'Your' : 'AI\'s'} turn`;
      case 'PLAYER_WIN':
        return 'Congratulations! You won! 🎉';
      case 'AI_WIN':
        return 'AI wins! Better luck next time!';
      case 'DRAW':
        return 'It\'s a draw! 🤝';
      default:
        return 'Unknown game state';
    }
  };

  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <GameContainer>
      <StatusText
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        key={gameState?.status}
      >
        {getStatusMessage()}
      </StatusText>

      {gameState && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <Board
            board={gameState.board}
            onCellClick={handleCellClick}
            disabled={isLoading || gameState.status !== 'IN_PROGRESS'}
          />
        </motion.div>
      )}

      <Button
        onClick={startNewGame}
        disabled={isLoading}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        New Game
      </Button>
    </GameContainer>
  );
};

export default Game;
