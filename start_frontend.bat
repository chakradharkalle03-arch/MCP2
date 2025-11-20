@echo off
REM Start Node.js Frontend Server
echo ========================================
echo Starting Node.js Frontend Server
echo ========================================
echo.

cd frontend
if exist node_modules (
    echo Node modules found. Starting server...
) else (
    echo Installing Node.js dependencies...
    call npm install
)

echo.
echo Frontend server starting on http://localhost:3000
echo Backend should be running on http://localhost:8001
echo.
echo Press Ctrl+C to stop
echo.

npm start

