#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display usage information
show_usage() {
    echo -e "${YELLOW}Usage:${NC} $0 [dev|prod]"
    echo -e "  dev  - Run the application in development mode"
    echo -e "  prod - Run the application in production mode (not implemented yet)"
    exit 1
}

# Function to run the application in development mode
run_dev() {
    echo -e "${GREEN}Starting Climetrics in development mode...${NC}"
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        echo -e "${RED}Error: uv is not installed. Please install it first.${NC}"
        echo -e "You can install it with: pip install uv"
        exit 1
    fi
    
    # Install backend dependencies
    echo -e "${YELLOW}Installing backend dependencies...${NC}"
    cd backend && uv pip install -r requirements.txt
    
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}Error: npm is not installed. Please install Node.js and npm first.${NC}"
        exit 1
    fi
    
    # Install frontend dependencies
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd ../frontend && npm install
    
    # Start both servers in parallel
    echo -e "${GREEN}Starting servers...${NC}"
    echo -e "${YELLOW}Django backend will be available at: ${GREEN}http://localhost:8000${NC}"
    echo -e "${YELLOW}React frontend will be available at: ${GREEN}http://localhost:3000${NC}"
    
    # Start the frontend and backend servers
    # Use terminal multiplexer or background processes
    (cd frontend && npm start) &
    FRONTEND_PID=$!
    
    (cd backend && uv run manage.py runserver) &
    BACKEND_PID=$!
    
    # Handle script termination
    trap "echo -e '${YELLOW}Shutting down servers...${NC}'; kill $FRONTEND_PID $BACKEND_PID; exit" SIGINT SIGTERM
    
    # Wait for both processes
    wait $FRONTEND_PID $BACKEND_PID
}

# Function to run the application in production mode (placeholder)
run_prod() {
    echo -e "${YELLOW}Production mode is not implemented yet.${NC}"
    echo -e "This would typically involve:"
    echo -e "  1. Building the React frontend"
    echo -e "  2. Collecting static files"
    echo -e "  3. Running Django with a production server like Gunicorn"
    echo -e "  4. Setting up a reverse proxy like Nginx"
    exit 0
}

# Main script logic
if [ $# -ne 1 ]; then
    show_usage
fi

case "$1" in
    dev)
        run_dev
        ;;
    prod)
        run_prod
        ;;
    *)
        show_usage
        ;;
esac 