# Project Summary: MCP-Based RAG System

## 🎯 Main Goal

**Demonstrate how MCP (Model Context Protocol) works and its purpose** through a working RAG (Retrieval-Augmented Generation) system for semiconductor component search.

## ✅ Requirements Implemented

### 1. ✅ MCP (Model Context Protocol)
- **MCP Server** (`mcp_server.py`): Implements MCP protocol for structured context retrieval
- **MCP Client** (`mcp_client_example.py`): Demonstrates how to use MCP for querying
- **Purpose**: Shows how MCP provides standardized tool-based interface for context retrieval

### 2. ✅ ChromaDB
- **Vector Database**: Used for storing and retrieving semantic embeddings
- **Collection**: `semiconductor_components` collection for document storage
- **Integration**: Fully integrated with RAG pipeline for semantic search

### 3. ✅ Llama Model (Decoding)
- **Primary**: Attempts to load `meta-llama/Llama-2-7b-chat-hf` from HuggingFace
- **Fallback**: Uses GPT-2 if Llama is not accessible
- **Purpose**: Generates answers based on retrieved context

### 4. ✅ Encoding Model (Embeddings)
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Purpose**: Converts text to embeddings for semantic search
- **Source**: HuggingFace Hub

### 5. ✅ Backend API
- **Framework**: FastAPI
- **Endpoints**:
  - `POST /upload`: Upload Excel documents
  - `POST /ask`: Ask questions and get answers
  - `GET /info`: Get collection information
  - `GET /health`: Health check
- **Features**: File upload, question-answering, RAG integration

### 6. ✅ RAG Flow with MCP
- **Document Processing**: Excel → Text chunks → Embeddings → ChromaDB
- **Query Processing**: Question → Embeddings → ChromaDB retrieval → LLM generation
- **MCP Integration**: Demonstrates MCP protocol for context retrieval

### 7. ✅ Example Excel Document
- **File**: `examples/semiconductor_components.xlsx`
- **Content**: 10 semiconductor components with details
- **Fields**: Component ID, Name, Category, Manufacturer, Part Number, Ratings, etc.

## 📁 Project Structure

```
MCP2/
├── main.py                    # FastAPI backend server
├── rag_pipeline.py           # RAG pipeline (embeddings + LLM)
├── mcp_server.py             # MCP server for ChromaDB
├── mcp_client_example.py     # Example MCP client usage
├── config.py                 # Configuration (API keys, models)
├── create_example_excel.py   # Generate example Excel file
├── test_api.py               # API testing script
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation
├── USAGE.md                  # Detailed usage guide
├── PROJECT_SUMMARY.md        # This file
├── .gitignore               # Git ignore rules
├── examples/                 # Example Excel files
│   └── semiconductor_components.xlsx
├── uploads/                  # Uploaded files (created at runtime)
└── chroma_db/               # ChromaDB storage (created at runtime)
```

## 🔄 How MCP Works in This Project

### MCP Purpose Demonstrated:

1. **Standardized Tool Interface**
   - MCP defines tools (`query_semiconductor_data`, `get_collection_info`)
   - Tools provide structured access to ChromaDB
   - Protocol-level abstraction for data retrieval

2. **Context Retrieval Flow**
   ```
   User Query
      ↓
   MCP Tool Call (query_semiconductor_data)
      ↓
   ChromaDB Semantic Search
      ↓
   Retrieved Context
      ↓
   LLM Answer Generation
   ```

3. **Protocol Benefits**
   - **Modularity**: MCP tools can be reused across different systems
   - **Standardization**: Consistent interface for context retrieval
   - **Extensibility**: Easy to add new tools or data sources

### MCP Implementation:

- **MCP Server**: Defines tools for ChromaDB operations
- **MCP Client**: Demonstrates tool discovery and usage
- **RAG Integration**: Uses MCP principles for context retrieval

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create example Excel:**
   ```bash
   python create_example_excel.py
   ```

3. **Start API server:**
   ```bash
   python main.py
   ```

4. **Upload document:**
   ```bash
   curl -X POST "http://localhost:8000/upload" \
     -F "file=@examples/semiconductor_components.xlsx"
   ```

5. **Ask question:**
   ```bash
   curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What MOSFET components are available?"}'
   ```

## 🔧 Technologies Used

- **MCP**: Model Context Protocol (v0.9.0)
- **ChromaDB**: Vector database (v0.4.18)
- **HuggingFace**: Models and Transformers
  - Encoding: `sentence-transformers/all-MiniLM-L6-v2`
  - Decoding: Llama-2 or GPT-2
- **FastAPI**: REST API framework
- **Python**: 3.8+
- **PyTorch**: Deep learning framework

## 📊 Data Flow

```
Excel Document
    ↓
Parse to Text Chunks
    ↓
Generate Embeddings (Encoding Model)
    ↓
Store in ChromaDB (with metadata)
    ↓
[User asks question]
    ↓
Generate Query Embedding
    ↓
Semantic Search in ChromaDB (MCP tool)
    ↓
Retrieve Relevant Context
    ↓
Generate Answer (LLM Decoding Model)
    ↓
Return Response
```

## 🎓 Key Concepts Demonstrated

1. **RAG (Retrieval-Augmented Generation)**
   - Retrieval phase: ChromaDB semantic search
   - Augmentation phase: Combine context with query
   - Generation phase: LLM generates answer

2. **MCP (Model Context Protocol)**
   - Tool-based interface
   - Standardized protocol
   - Context retrieval abstraction

3. **Semantic Search**
   - Embeddings for semantic similarity
   - Vector database for efficient retrieval
   - Metadata filtering capabilities

4. **Document Processing**
   - Excel parsing
   - Chunking strategy
   - Metadata preservation

## 📝 Example Questions

- "What MOSFET components are available?"
- "Show me voltage regulators from Texas Instruments"
- "What components work with 5V?"
- "List all temperature sensors"
- "What components are used for power switching?"

## 🔐 Configuration

HuggingFace API key should be set in `.env` file:
```python
HF_API_KEY=your_api_key_here
```

**Important**: Create a `.env` file in the root directory with your Hugging Face API key:
```
HF_API_KEY=your_api_key_here
```

Get your API key from: https://huggingface.co/settings/tokens

Models can be changed in `config.py`:
- `HF_EMBEDDING_MODEL`: Encoding model
- `HF_LLM_MODEL`: Decoding model
- `CHROMA_COLLECTION_NAME`: Collection name

## ✅ Testing

Run automated tests:
```bash
python test_api.py
```

Test MCP client:
```bash
python mcp_client_example.py
```

## 📚 Documentation

- **README.md**: Overview and installation
- **USAGE.md**: Detailed usage instructions
- **PROJECT_SUMMARY.md**: This file - project summary
- **API Docs**: Available at `http://localhost:8000/docs`

## 🎯 Project Goals Achieved

✅ **MCP Integration**: Fully implemented MCP server and client  
✅ **ChromaDB**: Vector database for semantic search  
✅ **HuggingFace Models**: Both encoding and decoding models  
✅ **RAG Flow**: Complete retrieval-augmented generation pipeline  
✅ **Backend API**: REST API for document upload and Q&A  
✅ **Example Data**: Semiconductor component Excel document  
✅ **Working System**: Fully functional end-to-end system  

## 🚦 Status

**Project Status**: ✅ **COMPLETE** and **WORKING**

All requirements have been implemented and the system is ready for demonstration and use.

