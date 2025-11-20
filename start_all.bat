@echo off
REM Start Both Backend and Frontend Servers
echo ========================================
echo Starting Both Servers
echo ========================================
echo.

echo Starting Backend Server...
start "Backend - Port 8001" cmd /k "cd /d %~dp0 && .\venv\Scripts\python.exe main.py"

timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
start "Frontend - Port 3000" cmd /k "cd /d %~dp0\frontend && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Open http://localhost:3000 in your browser
echo.
pause

