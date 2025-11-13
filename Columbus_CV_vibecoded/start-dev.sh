#!/bin/bash

echo "Starting Columbus CV Analyzer..."
echo

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "Creating .env file from template..."
    cp backend/.env.template backend/.env
    echo
    echo "IMPORTANT: Edit backend/.env and add your OPENAI_API_KEY"
    echo
    read -p "Press Enter to continue..."
fi

echo "Starting backend server..."
cd backend && python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "Starting frontend development server..."
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo
echo "Both servers are starting up:"
echo "- Backend: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers"

# Wait for user to interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait