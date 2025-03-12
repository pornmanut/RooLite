#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to kill process running on a specific port
kill_port() {
    local port=$1
    echo -n "Checking port $port... "
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}in use${NC}"
        echo -n "Attempting to kill process on port $port... "
        
        # Get PID of process using the port
        local pid=$(lsof -Pi :$port -sTCP:LISTEN -t)
        
        # Show process info before killing
        echo -e "\nProcess details:"
        ps -p $pid -o pid,ppid,user,%cpu,%mem,start,command
        
        # Kill the process
        kill -9 $pid 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Successfully killed process${NC}"
        else
            echo -e "${RED}Failed to kill process${NC}"
            echo -e "Try running: ${YELLOW}sudo $0${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}available${NC}"
    fi
}

# Kill processes on both development ports
echo -e "${YELLOW}Checking development ports...${NC}"
kill_port 8000  # Backend port
kill_port 3000  # Frontend port

echo -e "\n${GREEN}All ports have been checked and cleared if needed.${NC}"
echo "You can now run: make dev"
