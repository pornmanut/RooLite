# Tic-tac-toe Game Frontend

A modern React frontend for the Tic-tac-toe game with AI opponent.

## Features

- Modern React implementation with TypeScript
- Styled-components for styling
- Framer Motion for smooth animations
- Responsive design
- Clean and intuitive UI

## Setup

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Start the development server:
```bash
npm run start
# or
yarn start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
src/
├── components/        # React components
│   ├── Board.tsx     # Game board component
│   └── Game.tsx      # Main game component
├── services/         # API services
│   └── gameService.ts
├── types/           # TypeScript type definitions
│   └── game.ts
├── App.tsx         # Root component
└── main.tsx       # Application entry point
```

## Dependencies

- React 18+
- TypeScript
- Vite
- Styled Components
- Framer Motion
- Axios

## Development

The frontend is configured to proxy API requests to the backend server running on port 8000. Make sure the backend server is running before starting the frontend application.

## Building for Production

To create a production build:

```bash
npm run build
# or
yarn build
```

The built files will be in the `dist` directory.
