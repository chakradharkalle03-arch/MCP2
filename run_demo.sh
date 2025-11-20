#!/bin/bash
# Demo script to run the complete system

echo "=========================================="
echo "MCP + RAG Demo for Semiconductor Search"
echo "=========================================="
echo ""

# Create example Excel if not exists
if [ ! -f "examples/semiconductor_components.xlsx" ]; then
    echo "Creating example Excel file..."
    python create_example_excel.py
fi

echo ""
echo "Starting API server..."
echo "API will be available at http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python main.py

