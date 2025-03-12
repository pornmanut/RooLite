#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null
    return $?
}

# Function to wait for a service to be ready
wait_for_service() {
    local port=$1
    local service=$2
    local count=0
    local max_attempts=30

    echo -n "Waiting for $service to be ready "
    while ! nc -z localhost $port && [ $count -lt $max_attempts ]; do
        echo -n "."
        sleep 1
        ((count++))
    done
    echo ""

    if [ $count -eq $max_attempts ]; then
        echo -e "${RED}$service failed to start${NC}"
        return 1
    else
        echo -e "${GREEN}$service is ready${NC}"
        return 0
    fi
}

# Kill any processes using our ports
echo "Checking for existing processes..."
if check_port 8000; then
    echo -e "${YELLOW}Port 8000 is in use. Attempting to free it...${NC}"
    lsof -ti:8000 | xargs kill -9
fi

if check_port 3000; then
    echo -e "${YELLOW}Port 3000 is in use. Attempting to free it...${NC}"
    lsof -ti:3000 | xargs kill -9
fi

# Start backend
echo -e "${GREEN}Starting backend server...${NC}"
cd backend
python3 -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to be ready
if ! wait_for_service 8000 "Backend"; then
    kill $BACKEND_PID
    exit 1
fi

# Start frontend
echo -e "${GREEN}Starting frontend server...${NC}"
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to be ready
if ! wait_for_service 3000 "Frontend"; then
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 1
fi

echo -e "${GREEN}Both servers are running!${NC}"
echo -e "Frontend: ${YELLOW}http://localhost:3000${NC}"
echo -e "Backend API: ${YELLOW}http://localhost:8000${NC}"
echo -e "API Documentation: ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Wait for Ctrl+C and clean up
trap 'echo -e "\n${YELLOW}Shutting down servers...${NC}"; kill $BACKEND_PID $FRONTEND_PID; exit 0' INT

wait
