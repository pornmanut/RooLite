import React from 'react';
import { createGlobalStyle } from 'styled-components';
import Game from './components/Game';

const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background: #ecf0f1;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
`;

const App: React.FC = () => {
  return (
    <>
      <GlobalStyle />
      <Game />
    </>
  );
};

export default App;
