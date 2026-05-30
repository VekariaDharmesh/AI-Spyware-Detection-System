#!/bin/bash

# Color styles for modern terminal logging
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}   🛡️  SILENTGUARD AI 2.0 - FUTURISTIC CYBER COMMAND CENTER  🛡️   ${NC}"
echo -e "${CYAN}================================================================${NC}"

# Check for required python and node commands
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] python3 is not installed or not in PATH.${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}[ERROR] npm is not installed or not in PATH.${NC}"
    exit 1
fi

# Store the PIDs of backgrounded processes so we can clean them up on exit
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo -e "\n${RED}[SHUTDOWN] Terminating active processes...${NC}"
    if [ -n "$BACKEND_PID" ]; then
        echo -e "${RED}• Stopping Python FastAPI Server (PID: $BACKEND_PID)...${NC}"
        kill -9 "$BACKEND_PID" 2>/dev/null
    fi
    if [ -n "$FRONTEND_PID" ]; then
        echo -e "${RED}• Stopping Next.js React Dashboard (PID: $FRONTEND_PID)...${NC}"
        kill -9 "$FRONTEND_PID" 2>/dev/null
    fi
    echo -e "${GREEN}[SHUTDOWN] Cleanup finished. Command Center Offline.${NC}"
    exit 0
}

# Trap Ctrl+C (SIGINT) and exit signals to run cleanup
trap cleanup SIGINT SIGTERM EXIT

# Start 1: Python FastAPI Backend REST Engine
echo -e "${CYAN}[BACKEND] Launching Local FastAPI Security Core...${NC}"
cd spyware_detection_project || { echo -e "${RED}[ERROR] Folder spyware_detection_project not found.${NC}"; exit 1; }
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Give the backend a brief moment to bind and launch
sleep 2

# Verify backend is running
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}[BACKEND] REST Engine is ONLINE at http://localhost:8000 ✅${NC}"
else
    echo -e "${RED}[ERROR] FastAPI failed to boot. Check logs above.${NC}"
    exit 1
fi

# Start 2: Next.js Frontend React Server
echo -e "${CYAN}[FRONTEND] Launching Next.js Cyber Dashboard...${NC}"
if [ ! -d "frontend" ]; then
    echo -e "${RED}[ERROR] Next.js frontend folder not found. Scaffolding may still be in progress!${NC}"
    exit 1
fi

cd frontend || exit 1
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 2

# Verify frontend is running
if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}[FRONTEND] Futuristic Cyber UI is ONLINE at http://localhost:3000 ✅${NC}"
    echo -e "${CYAN}================================================================${NC}"
    echo -e "${GREEN}Command Center initialized! Open your browser at http://localhost:3000${NC}"
    echo -e "${CYAN}Press [Ctrl+C] at any time to shut down the servers.${NC}"
    echo -e "${CYAN}================================================================${NC}"
else
    echo -e "${RED}[ERROR] Next.js failed to boot. Check logs above.${NC}"
    exit 1
fi

# Keep script running to maintain logs and wait for Ctrl+C
while true; do
    sleep 1
done
