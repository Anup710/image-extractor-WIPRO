@echo off
echo Starting Columbus CV Analyzer...
echo.

echo Checking if .env exists...
if not exist "backend\.env" (
    echo Creating .env file from template...
    copy "backend\.env.template" "backend\.env"
    echo.
    echo IMPORTANT: Edit backend\.env and add your OPENAI_API_KEY
    echo.
    pause
)

echo Starting backend server...
start "Backend Server" cmd /c "cd backend && python main.py"

timeout /t 3 /nobreak >nul

echo Starting frontend development server...
start "Frontend Server" cmd /c "cd frontend && npm run dev"

echo.
echo Both servers are starting up:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo Check the console windows for any errors.
pause