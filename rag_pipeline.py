"""
RAG Pipeline for Semiconductor Component Search
Handles embedding generation and LLM inference
"""
import os
from typing import List, Dict, Any
import pandas as pd
import config

# Import dependencies with error handling
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except Exception as e:
    print(f"Warning: ChromaDB import failed: {e}")
    CHROMADB_AVAILABLE = False
    
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except Exception as e:
    print(f"Warning: sentence-transformers import failed: {e}")
    print("This might be due to DLL issues on Windows. Try installing Visual C++ Redistributables.")
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except Exception as e:
    print(f"Warning: transformers import failed: {e}")
    TRANSFORMERS_AVAILABLE = False

from huggingface_hub import login

# Authenticate with Hugging Face
try:
    login(token=config.HF_API_KEY)
except Exception as e:
    print(f"Warning: HuggingFace login failed: {e}")

# Initialize ChromaDB - Lazy loading to avoid onnxruntime issues
chroma_client = None
collection = None

def _init_chromadb():
    """Initialize ChromaDB client and collection"""
    global chroma_client, collection
    if not CHROMADB_AVAILABLE:
        raise ImportError("ChromaDB is not available. Please check your installation.")
    
    if chroma_client is None:
        try:
            chroma_client = chromadb.PersistentClient(
                path=config.CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False, allow_reset=True)
            )
            # Create collection - we'll provide our own embeddings
            collection = chroma_client.get_or_create_collection(
                name=config.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            raise
    return chroma_client, collection


class RAGPipeline:
    """RAG Pipeline for document processing and question answering"""
    
    def __init__(self):
        self.encoder = None
        self.use_embeddings = False
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                print("Loading embedding model...")
                # Encoding model - for creating embeddings
                self.encoder = SentenceTransformer(config.HF_EMBEDDING_MODEL)
                print(f"Loaded encoder: {config.HF_EMBEDDING_MODEL}")
                self.use_embeddings = True
            except Exception as e:
                print(f"Warning: Could not load embedding model: {e}")
                print("Will use text-based search instead")
                self.use_embeddings = False
        else:
            print("Warning: sentence-transformers not available. Using text-based search.")
            self.use_embeddings = False
        
        print("Loading LLM model...")
        # Decoding model - for generating answers
        # Try Llama first, then fallback to GPT-2
        self.use_pipeline = None
        self.generator = None
        self.tokenizer = None
        self.llm = None
        
        if TRANSFORMERS_AVAILABLE:
            # Try to load Llama model
            llama_model = "meta-llama/Llama-2-7b-chat-hf"
            try:
                print(f"Attempting to load {llama_model}...")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    llama_model,
                    token=config.HF_API_KEY,
                    trust_remote_code=True
                )
                self.llm = AutoModelForCausalLM.from_pretrained(
                    llama_model,
                    token=config.HF_API_KEY,
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None,
                    low_cpu_mem_usage=True
                )
                self.use_pipeline = False
                print(f"Successfully loaded {llama_model}")
            except Exception as e:
                print(f"Could not load Llama model: {e}")
                print("Using GPT-2 as fallback...")
                # Fallback to GPT-2 which is more accessible
                try:
                    self.generator = pipeline(
                        "text-generation",
                        model="gpt2",
                        tokenizer="gpt2",
                        token=config.HF_API_KEY,
                        device=0 if torch.cuda.is_available() else -1
                    )
                    self.use_pipeline = True
                    print("Using GPT-2 as generation model")
                except Exception as e2:
                    print(f"Error loading GPT-2: {e2}")
                    print("Will use simple context-based responses")
                    self.use_pipeline = None
        else:
            print("Transformers not available. Will use simple context-based responses")
            self.use_pipeline = None
        
        print("RAG Pipeline initialized!")
    
    def process_excel(self, file_path: str) -> List[Dict[str, Any]]:
        """Process Excel file and extract text chunks"""
        try:
            df = pd.read_excel(file_path)
            
            # Convert DataFrame to text chunks
            chunks = []
            for idx, row in df.iterrows():
                # Create a text representation of each row
                row_text = f"Component: {row.to_dict()}"
                chunks.append({
                    "text": str(row_text),
                    "metadata": {
                        "row_index": idx,
                        "source": file_path,
                        **{str(k): str(v) for k, v in row.to_dict().items()}
                    }
                })
            
            return chunks
        except Exception as e:
            raise Exception(f"Error processing Excel file: {str(e)}")
    
    def store_documents(self, chunks: List[Dict[str, Any]]):
        """Store document chunks in ChromaDB with embeddings"""
        global collection
        _init_chromadb()
        
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [f"doc_{i}" for i in range(len(chunks))]
        
        if self.use_embeddings and self.encoder is not None:
            # Generate embeddings using the encoder model
            print(f"Generating embeddings for {len(texts)} chunks...")
            try:
                embeddings = self.encoder.encode(texts).tolist()
                # Store in ChromaDB with embeddings
                collection.add(
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Stored {len(chunks)} documents in ChromaDB with embeddings")
            except Exception as e:
                print(f"Error generating embeddings: {e}, falling back to text search")
                self.use_embeddings = False
                # Fallback to text search
                collection.add(
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Stored {len(chunks)} documents in ChromaDB (text search mode)")
        else:
            # Store without embeddings - use text search
            print(f"Storing {len(texts)} chunks using text search...")
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Stored {len(chunks)} documents in ChromaDB (text search mode)")
    
    def retrieve_context(self, query: str, n_results: int = 5) -> List[str]:
        """Retrieve relevant context from ChromaDB"""
        global collection
        _init_chromadb()
        
        if self.use_embeddings and self.encoder is not None:
            try:
                # Generate query embedding
                query_embedding = self.encoder.encode([query]).tolist()[0]
                
                # Query ChromaDB with embeddings
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results
                )
            except Exception as e:
                print(f"Error with embedding search: {e}, falling back to text search")
                # Fallback to text search
                results = collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
        else:
            # Use text-based search
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
        
        if results['documents'] and len(results['documents'][0]) > 0:
            return results['documents'][0]
        return []
    
    def generate_answer(self, query: str, context: List[str]) -> str:
        """Generate answer using LLM with retrieved context"""
        # Format context
        context_text = "\n\n".join([f"Context {i+1}: {ctx}" for i, ctx in enumerate(context)])
        
        # Create prompt
        prompt = f"""Based on the following context about semiconductor components, answer the question.

Context:
{context_text}

Question: {query}

Answer:"""
        
        try:
            if self.use_pipeline and hasattr(self, 'generator'):
                # Use pipeline for generation (GPT-2)
                response = self.generator(
                    prompt,
                    max_length=min(len(prompt.split()) + 100, 512),
                    num_return_sequences=1,
                    temperature=0.7,
                    truncation=True,
                    pad_token_id=self.generator.tokenizer.eos_token_id
                )
                answer = response[0]['generated_text'].replace(prompt, "").strip()
                if not answer:
                    answer = self._extract_from_context(context, query)
            
            elif hasattr(self, 'llm') and not self.use_pipeline:
                # Use LLM directly (Llama)
                inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
                if torch.cuda.is_available() and hasattr(self.llm, 'cuda'):
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.llm.generate(
                        **inputs,
                        max_new_tokens=150,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id if hasattr(self.tokenizer, 'eos_token_id') else self.tokenizer.pad_token_id
                    )
                
                answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                answer = answer.replace(prompt, "").strip()
                if not answer:
                    answer = self._extract_from_context(context, query)
            else:
                # Fallback to context-based answer
                answer = self._extract_from_context(context, query)
        
        except Exception as e:
            print(f"Error in generation: {e}")
            answer = self._extract_from_context(context, query)
        
        return answer
    
    def _extract_from_context(self, context: List[str], query: str) -> str:
        """Extract relevant information from context as fallback"""
        # Simple extraction based on keywords
        query_lower = query.lower()
        relevant_parts = []
        
        for ctx in context:
            if any(word in ctx.lower() for word in query_lower.split() if len(word) > 3):
                relevant_parts.append(ctx[:300])  # Limit length
        
        if relevant_parts:
            return f"Based on the retrieved information:\n\n" + "\n\n".join(relevant_parts[:3])
        else:
            return "\n\n".join([f"- {ctx[:200]}" for ctx in context[:3]])
    
    def answer_question(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve context and generate answer"""
        # Retrieve relevant context
        context = self.retrieve_context(query, n_results)
        
        if not context:
            return {
                "answer": "I couldn't find any relevant information in the database. Please upload a document first.",
                "context": [],
                "query": query
            }
        
        # Generate answer
        answer = self.generate_answer(query, context)
        
        return {
            "answer": answer,
            "context": context,
            "query": query
        }


# Global instance
rag_pipeline = None

def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline instance"""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline

