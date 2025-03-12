import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Board as BoardType, Player } from '@/types/game';

const BoardContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  background-color: #2c3e50;
  padding: 8px;
  border-radius: 8px;
  width: 300px;
  height: 300px;
`;

const Cell = styled(motion.button)`
  background-color: #34495e;
  border: none;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
  cursor: pointer;
  aspect-ratio: 1;

  &:hover {
    background-color: #2980b9;
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.7;
  }
`;

interface BoardProps {
  board: BoardType;
  onCellClick: (row: number, col: number) => void;
  disabled: boolean;
}

export const Board: React.FC<BoardProps> = ({ board, onCellClick, disabled }) => {
  const cellVariants = {
    initial: { scale: 0 },
    animate: { scale: 1 },
    exit: { scale: 0 }
  };

  return (
    <BoardContainer>
      {board.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <Cell
            key={`${rowIndex}-${colIndex}`}
            onClick={() => onCellClick(rowIndex, colIndex)}
            disabled={cell !== ' ' || disabled}
            initial="initial"
            animate="animate"
            exit="exit"
            variants={cellVariants}
            whileHover={{ scale: 0.95 }}
            whileTap={{ scale: 0.9 }}
          >
            {cell !== ' ' && (
              <motion.span
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2 }}
              >
                {cell}
              </motion.span>
            )}
          </Cell>
        ))
      )}
    </BoardContainer>
  );
};

export default Board;
