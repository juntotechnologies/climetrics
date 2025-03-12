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

# Function to kill processes on specific ports
kill_process_on_port() {
    local port=$1
    local pid=$(lsof -t -i:$port)
    
    if [ -n "$pid" ]; then
        echo -e "${YELLOW}Found process using port $port (PID: $pid). Killing it...${NC}"
        kill -9 $pid 2>/dev/null
        sleep 1
    fi
}

# Function to run the application in development mode
run_dev() {
    echo -e "${GREEN}Starting Climetrics in development mode...${NC}"
    
    # Store the root directory
    ROOT_DIR="$(pwd)"
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        echo -e "${RED}Error: uv is not installed. Please install it first.${NC}"
        echo -e "You can install it with: pip install uv"
        exit 1
    fi
    
    # Kill any processes using port 8000
    echo -e "${YELLOW}Checking for processes using port 8000...${NC}"
    kill_process_on_port 8000
    
    # Install backend dependencies
    echo -e "${YELLOW}Installing backend dependencies...${NC}"
    (cd "${ROOT_DIR}/backend" && uv pip install -r requirements.txt)
    
    # Start the Django server
    echo -e "${GREEN}Starting Django server...${NC}"
    echo -e "${YELLOW}Application will be available at: ${GREEN}http://localhost:8000${NC}"
    
    # Run Django server
    (cd "${ROOT_DIR}/backend" && uv run manage.py runserver)
}

# Function to run the application in production mode (placeholder)
run_prod() {
    echo -e "${YELLOW}Production mode is not implemented yet.${NC}"
    echo -e "This would typically involve:"
    echo -e "  1. Collecting static files"
    echo -e "  2. Running Django with a production server like Gunicorn"
    echo -e "  3. Setting up a reverse proxy like Nginx"
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