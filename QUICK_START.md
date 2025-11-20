# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Example Data
```bash
python create_example_excel.py
```

### Step 3: Start the Server
```bash
python main.py
```

The API will be available at: **http://localhost:8000**

## 📤 Upload Document

Open browser: **http://localhost:8000/docs**

Or use curl:
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@examples/semiconductor_components.xlsx"
```

## ❓ Ask Questions

**Via Browser:**
- Go to http://localhost:8000/docs
- Click on `/ask` endpoint
- Click "Try it out"
- Enter question: `"What MOSFET components are available?"`
- Click "Execute"

**Via curl:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What MOSFET components are available?", "n_results": 3}'
```

## 🎯 Example Questions

- "What MOSFET components are available?"
- "Show me voltage regulators"
- "What components work with 5V?"
- "List components from Texas Instruments"

## 📚 Full Documentation

- **README.md** - Overview
- **USAGE.md** - Detailed usage
- **PROJECT_SUMMARY.md** - Complete project details

## ✅ Verify Setup

```bash
# Check API health
curl http://localhost:8000/health

# Check collection info
curl http://localhost:8000/info

# Run automated tests
python test_api.py
```

## 🎓 Understanding MCP

**MCP Purpose**: Standardized protocol for context retrieval

**How it works here:**
1. MCP Server defines tools for ChromaDB access
2. RAG Pipeline uses MCP principles for retrieval
3. Questions trigger MCP tool calls → ChromaDB → LLM → Answer

See `PROJECT_SUMMARY.md` for detailed explanation!

