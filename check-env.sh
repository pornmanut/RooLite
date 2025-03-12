#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Checking development environment...${NC}\n"

# Check Python version
echo -n "Checking Python version... "
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi

# Check Node.js version
echo -n "Checking Node.js version... "
if command -v node &>/dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found${NC}"
    exit 1
fi

# Check npm version
echo -n "Checking npm version... "
if command -v npm &>/dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm not found${NC}"
    exit 1
fi

# Check if required ports are available
echo -n "Checking if port 8000 is available (backend)... "
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}✗ Port 8000 is in use${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Available${NC}"
fi

echo -n "Checking if port 3000 is available (frontend)... "
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}✗ Port 3000 is in use${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Available${NC}"
fi

# Check if required directories exist
echo -n "Checking project structure... "
if [ -d "backend" ] && [ -d "frontend" ]; then
    echo -e "${GREEN}✓ Directories found${NC}"
else
    echo -e "${RED}✗ Missing required directories${NC}"
    exit 1
fi

echo -e "\n${GREEN}✓ Environment check completed successfully!${NC}"
echo -e "${YELLOW}You can now run 'make install' to set up the project.${NC}"
