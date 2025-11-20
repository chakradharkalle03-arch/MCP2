# MCP-Based RAG System for Semiconductor Component Search

This project demonstrates **MCP (Model Context Protocol)** integration with ChromaDB and HuggingFace models for Retrieval-Augmented Generation (RAG).

## Project Overview

This system shows how **MCP works** and its **purpose**:
- **MCP** provides a standardized protocol for context retrieval
- **ChromaDB** stores and retrieves semantic embeddings
- **RAG Pipeline** combines retrieval with LLM generation
- **Backend API** allows document upload and question-answering

## Architecture

```
User Question → API Endpoint → RAG Pipeline
                                    ↓
                    Retrieval from ChromaDB (via embeddings)
                                    ↓
                    LLM generates answer with context
                                    ↓
                    Response to user
```

### Key Components

1. **MCP Server** (`mcp_server.py`): Demonstrates MCP protocol for structured context retrieval
2. **RAG Pipeline** (`rag_pipeline.py`): Handles embeddings (encoding) and LLM (decoding)
3. **FastAPI Backend** (`main.py`): REST API for document upload and Q&A
4. **ChromaDB**: Vector database for semantic search

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
Create a `.env` file or use the provided HF API key in `config.py`

3. **Create example Excel file:**
```bash
python create_example_excel.py
```

## Usage

### 1. Start the API Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Upload Excel Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -F "file=@examples/semiconductor_components.xlsx"
```

Or use the FastAPI docs at `http://localhost:8000/docs`

### 3. Ask Questions

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What MOSFET components are available?", "n_results": 3}'
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /upload` - Upload Excel document
- `POST /ask` - Ask a question
- `GET /info` - Get collection information

## How MCP Works

**MCP (Model Context Protocol)** serves as a standardized interface for:
- **Context Retrieval**: Structured way to query and retrieve relevant information
- **Tool Definition**: Clear specification of available operations
- **Protocol Communication**: Standardized communication between components

In this project:
1. MCP server defines tools for querying ChromaDB
2. RAG pipeline uses MCP principles for context retrieval
3. Backend integrates MCP concepts for document processing

## Models Used

- **Encoding (Embeddings)**: `sentence-transformers/all-MiniLM-L6-v2`
- **Decoding (LLM)**: Llama model from HuggingFace (or fallback to GPT-2)

## Example Questions

- "What MOSFET components are available?"
- "Show me voltage regulators from Texas Instruments"
- "What components work with 5V?"
- "List all temperature sensors"

## Project Structure

```
MCP2/
├── main.py                 # FastAPI backend
├── rag_pipeline.py         # RAG pipeline with embeddings & LLM
├── mcp_server.py          # MCP server for ChromaDB
├── config.py              # Configuration
├── create_example_excel.py # Generate example data
├── requirements.txt       # Dependencies
├── examples/              # Example Excel files
└── chroma_db/            # ChromaDB storage (created automatically)
```

## Notes

- First run will download models from HuggingFace (requires API key)
- ChromaDB data persists in `./chroma_db/` directory
- Uploaded files are stored in `./uploads/` directory

