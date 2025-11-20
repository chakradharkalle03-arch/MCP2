# Usage Guide - MCP-Based RAG System

This guide demonstrates how to use the MCP (Model Context Protocol) integrated RAG system.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Example Data

```bash
python create_example_excel.py
```

This creates `examples/semiconductor_components.xlsx` with sample data.

### 3. Start the API Server

**Windows:**
```bash
python main.py
```

**Or use the batch script:**
```bash
run_demo.bat
```

**Linux/Mac:**
```bash
./run_demo.sh
```

The API will start at `http://localhost:8000`

### 4. Access API Documentation

Open your browser and go to:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Step-by-Step Usage

### Step 1: Upload Excel Document

**Using curl:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -F "file=@examples/semiconductor_components.xlsx"
```

**Using Python:**
```python
import requests

url = "http://localhost:8000/upload"
files = {"file": open("examples/semiconductor_components.xlsx", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**Response:**
```json
{
  "message": "File uploaded and processed successfully",
  "filename": "semiconductor_components.xlsx",
  "chunks_processed": 10,
  "status": "ready_for_queries"
}
```

### Step 2: Ask Questions

**Using curl:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What MOSFET components are available?", "n_results": 3}'
```

**Using Python:**
```python
import requests

url = "http://localhost:8000/ask"
payload = {
    "question": "What MOSFET components are available?",
    "n_results": 3
}
response = requests.post(url, json=payload)
print(response.json())
```

**Response:**
```json
{
  "answer": "Based on the retrieved information...",
  "context": ["Context chunks..."],
  "query": "What MOSFET components are available?"
}
```

### Step 3: Check Collection Info

```bash
curl http://localhost:8000/info
```

## Example Questions

Try these questions:

1. **"What MOSFET components are available?"**
   - Retrieves MOSFET-related components

2. **"Show me voltage regulators"**
   - Finds voltage regulator components

3. **"What components work with 5V?"**
   - Searches for 5V compatible components

4. **"List components from Texas Instruments"**
   - Filters by manufacturer

5. **"What temperature sensors are available?"**
   - Finds temperature sensor components

6. **"Show me components for power switching"**
   - Searches by application

## Testing the System

### Run Automated Tests

```bash
python test_api.py
```

This will:
1. Test health endpoint
2. Upload example Excel file
3. Test question answering
4. Verify collection info

### Test MCP Client (Optional)

The MCP client demonstrates how MCP protocol works:

```bash
python mcp_client_example.py
```

**Note:** Requires data to be loaded in ChromaDB first.

## Understanding MCP in This Project

### What is MCP?

**MCP (Model Context Protocol)** provides:
- **Standardized tool interface** for context retrieval
- **Protocol-level abstraction** for data access
- **Structured communication** between AI models and data sources

### How MCP Works Here

1. **MCP Server** (`mcp_server.py`):
   - Defines tools for querying ChromaDB
   - Provides standardized interface for context retrieval
   - Demonstrates MCP protocol structure

2. **RAG Pipeline** (`rag_pipeline.py`):
   - Uses MCP principles for retrieval
   - Integrates with ChromaDB via embeddings
   - Generates answers using LLM

3. **API Backend** (`main.py`):
   - Exposes REST endpoints
   - Uses RAG pipeline for Q&A
   - Demonstrates end-to-end MCP flow

### MCP Flow Diagram

```
User Question
    ↓
FastAPI Endpoint (/ask)
    ↓
RAG Pipeline
    ↓
┌─────────────────────────────────┐
│  MCP Context Retrieval          │
│  1. Query → Embeddings          │
│  2. Embeddings → ChromaDB       │
│  3. Retrieve Relevant Context   │
└─────────────────────────────────┘
    ↓
LLM Generation
    ↓
Answer to User
```

## Troubleshooting

### Issue: Models not loading

**Solution:** 
- Ensure HuggingFace API key is set correctly
- Check internet connection for model downloads
- First run may take time to download models

### Issue: ChromaDB errors

**Solution:**
- Delete `chroma_db/` folder and restart
- Ensure write permissions in project directory

### Issue: Excel file not processing

**Solution:**
- Ensure file is `.xlsx` or `.xls` format
- Check file is not corrupted
- Verify pandas and openpyxl are installed

### Issue: API not responding

**Solution:**
- Check if port 8000 is available
- Verify all dependencies are installed
- Check error logs in terminal

## Advanced Usage

### Custom Embedding Model

Edit `config.py`:
```python
HF_EMBEDDING_MODEL = "sentence-transformers/your-model"
```

### Custom LLM Model

Edit `config.py`:
```python
HF_LLM_MODEL = "your-huggingface-model"
```

### Change ChromaDB Collection

Edit `config.py`:
```python
CHROMA_COLLECTION_NAME = "your_collection_name"
```

## Next Steps

1. **Add more documents**: Upload multiple Excel files
2. **Experiment with queries**: Try different question formats
3. **Customize models**: Use different embedding/LLM models
4. **Extend MCP tools**: Add more tools to MCP server
5. **Build frontend**: Create a web interface

## Support

For issues or questions:
1. Check error logs in terminal
2. Verify all dependencies are installed
3. Ensure HuggingFace API key is valid
4. Check ChromaDB collection has data

