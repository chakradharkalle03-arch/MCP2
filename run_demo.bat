@echo off
REM Demo script for Windows to run the complete system

echo ==========================================
echo MCP + RAG Demo for Semiconductor Search
echo ==========================================
echo.

REM Create example Excel if not exists
if not exist "examples\semiconductor_components.xlsx" (
    echo Creating example Excel file...
    python create_example_excel.py
)

echo.
echo Starting API server...
echo API will be available at http://localhost:8000
echo Press Ctrl+C to stop
echo.

python main.py

