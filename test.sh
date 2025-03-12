#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running Backend Tests...${NC}"
cd backend
python3 -m pytest

# Store the backend test result
BACKEND_RESULT=$?

echo -e "\n${GREEN}Running Frontend Tests...${NC}"
cd ../frontend
npm test

# Store the frontend test result
FRONTEND_RESULT=$?

# Check if any tests failed
if [ $BACKEND_RESULT -eq 0 ] && [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed successfully!${NC}"
    exit 0
else
    echo -e "\n${RED}✗ Some tests failed!${NC}"
    exit 1
fi
