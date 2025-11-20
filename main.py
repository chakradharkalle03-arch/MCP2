"""
FastAPI Backend for Semiconductor Component Search
Demonstrates MCP integration with ChromaDB and RAG
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from pathlib import Path
from rag_pipeline import get_rag_pipeline
import config

app = FastAPI(
    title="Semiconductor Component Search API",
    description="RAG-based search using MCP, ChromaDB, and HuggingFace models",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Create static directory if it doesn't exist
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)


class QuestionRequest(BaseModel):
    question: str
    n_results: Optional[int] = 5


class QuestionResponse(BaseModel):
    answer: str
    context: list
    query: str


@app.get("/")
async def root():
    """Serve the main UI page"""
    html_path = Path("static/index.html")
    if html_path.exists():
        return FileResponse(str(html_path), media_type="text/html")
    else:
        return {
            "message": "Semiconductor Component Search API",
            "description": "This API demonstrates MCP (Model Context Protocol) integration with ChromaDB and RAG",
            "ui": "Visit http://localhost:8001/docs for API documentation",
            "endpoints": {
                "/upload": "POST - Upload Excel document",
                "/ask": "POST - Ask a question about uploaded documents",
                "/health": "GET - Health check",
                "/info": "GET - Get collection information"
            }
        }

# Mount static files after routes
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Semiconductor Component Search API",
        "description": "This API demonstrates MCP (Model Context Protocol) integration with ChromaDB and RAG",
        "endpoints": {
            "/upload": "POST - Upload Excel document",
            "/ask": "POST - Ask a question about uploaded documents",
            "/health": "GET - Health check",
            "/info": "GET - Get collection information"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "semiconductor-search-api"}


@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    """
    Upload an Excel document and process it for RAG
    This stores the document in ChromaDB with embeddings
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an Excel file (.xlsx or .xls)"
        )
    
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process with RAG pipeline
        rag = get_rag_pipeline()
        chunks = rag.process_excel(str(file_path))
        rag.store_documents(chunks)
        
        return {
            "message": "File uploaded and processed successfully",
            "filename": file.filename,
            "chunks_processed": len(chunks),
            "status": "ready_for_queries"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an answer using RAG
    This demonstrates the MCP flow:
    1. Query is processed through the RAG pipeline
    2. Context is retrieved from ChromaDB (via embeddings)
    3. LLM generates answer based on retrieved context
    """
    try:
        rag = get_rag_pipeline()
        result = rag.answer_question(request.question, request.n_results)
        
        return QuestionResponse(
            answer=result["answer"],
            context=result["context"],
            query=result["query"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.get("/info")
async def get_info():
    """Get information about the ChromaDB collection"""
    try:
        from rag_pipeline import _init_chromadb
        _, collection = _init_chromadb()
        count = collection.count()
        return {
            "collection_name": config.CHROMA_COLLECTION_NAME,
            "document_count": count,
            "status": "active"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("Starting Semiconductor Component Search API")
    print("="*50)
    print(f"API will be available at http://{config.API_HOST}:{config.API_PORT}")
    print(f"MCP demonstrates how context retrieval works through standardized protocols")
    print("="*50 + "\n")
    
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )

