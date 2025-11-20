import os
from dotenv import load_dotenv

load_dotenv()

# Hugging Face Configuration
# IMPORTANT: Set your Hugging Face API key in .env file or environment variable
# Get your API key from: https://huggingface.co/settings/tokens
HF_API_KEY = os.getenv("HF_API_KEY", "")
if not HF_API_KEY:
    raise ValueError("HF_API_KEY not found! Please set it in .env file or environment variable.")
HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Lightweight and efficient
# Using a smaller, more accessible model - can be swapped for Llama if available
HF_LLM_MODEL = "microsoft/DialoGPT-medium"  # Alternative: "meta-llama/Llama-2-7b-chat-hf"

# ChromaDB Configuration
CHROMA_PERSIST_DIR = "./chroma_db"
CHROMA_COLLECTION_NAME = "semiconductor_components"

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8001  # Changed to 8001 to avoid conflicts

