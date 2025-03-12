#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Error handling
set -e  # Exit on error
trap 'echo -e "\n${RED}An error occurred. Exiting...${NC}"; kill $(jobs -p) 2>/dev/null; exit 1' ERR

# Kill process on a port
kill_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}Port $port in use. Killing process...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
}

# Ensure we're in the project root directory
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo -e "${RED}Error: Must be run from project root directory${NC}"
    exit 1
fi

# Main script
echo -e "${GREEN}Setting up Tic-tac-toe game servers...${NC}"

# 1. Kill existing processes
echo "Checking ports..."
kill_port 8000
kill_port 3000

# 2. Start backend
echo -e "\n${GREEN}Starting backend server...${NC}"
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi
./venv/bin/uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# 3. Start frontend
echo -e "\n${GREEN}Starting frontend server...${NC}"
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting Vite development server..."
npm run dev &
FRONTEND_PID=$!

# Wait a moment to ensure servers are starting
sleep 2

# Check if processes are running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}Backend server failed to start${NC}"
    exit 1
fi

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}Frontend server failed to start${NC}"
    kill $BACKEND_PID
    exit 1
fi

# Print status
echo -e "\n${GREEN}All servers started successfully!${NC}"
echo -e "Frontend: ${YELLOW}http://localhost:3000${NC}"
echo -e "Backend API: ${YELLOW}http://localhost:8000${NC}"
echo -e "API docs: ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Handle cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

# Wait for processes
wait
