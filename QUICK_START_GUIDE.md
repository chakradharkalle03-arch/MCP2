# 🚀 Quick Start Guide

## ✅ Repository Pushed Successfully!

Your MCP-based RAG system is now on GitHub:
**https://github.com/chakradharkalle03-arch/MCP2**

---

## 📦 What's Included

- ✅ **50 files** committed and pushed
- ✅ **MCP (Model Context Protocol)** integration
- ✅ **ChromaDB** vector database
- ✅ **FastAPI** backend
- ✅ **Node.js/Express** frontend
- ✅ **RAG pipeline** with HuggingFace models
- ✅ **Complete documentation**

---

## 🎯 Quick Setup (3 Steps)

### Step 1: Clone the Repository

```bash
git clone https://github.com/chakradharkalle03-arch/MCP2.git
cd MCP2
```

### Step 2: Set Up Environment

**Backend (Python):**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy env.example .env
# Then edit .env and add your Hugging Face API key:
# HF_API_KEY=your_api_key_here
```

**Frontend (Node.js):**
```bash
cd frontend
npm install
cd ..
```

### Step 3: Run the Application

**Option A: Run Both Servers (Recommended)**
```bash
# Windows:
start_all.bat

# Linux/Mac:
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend
cd frontend && node server.js
```

**Option B: Run Separately**

**Backend:**
```bash
python main.py
# Backend runs on: http://localhost:8001
```

**Frontend:**
```bash
cd frontend
node server.js
# Frontend runs on: http://localhost:3000
```

---

## 🌐 Access the Application

**Frontend UI:** http://localhost:3000  
**Backend API:** http://localhost:8001

---

## 📝 First Steps

1. **Add Your API Key**
   - Get your Hugging Face API key from: https://huggingface.co/settings/tokens
   - Add it to `.env` file:
     ```
     HF_API_KEY=your_api_key_here
     ```

2. **Create Example Data**
   ```bash
   python create_example_excel.py
   ```

3. **Upload Document**
   - Go to http://localhost:3000
   - Click "Upload Excel Document"
   - Select the generated `semiconductor_components.xlsx`

4. **Ask Questions**
   - Type your question in the input field
   - Examples:
     - "Show me all voltage regulators"
     - "What components are used for power switching?"
     - "List temperature sensors"

---

## 📚 Documentation Files

- `README.md` - Main documentation
- `QUICK_START.md` - Detailed quick start
- `USAGE.md` - API usage guide
- `FRONTEND_GUIDE.md` - Frontend documentation
- `SETUP_WINDOWS.md` - Windows-specific setup

---

## 🎉 You're All Set!

Your MCP-based RAG system is ready to use!

**Repository:** https://github.com/chakradharkalle03-arch/MCP2  
**Issues:** https://github.com/chakradharkalle03-arch/MCP2/issues  
**Pull Requests:** https://github.com/chakradharkalle03-arch/MCP2/pulls

---

## 🔧 Troubleshooting

### Port Already in Use
If port 8001 or 3000 is in use, change them in:
- Backend: `config.py` → `API_PORT`
- Frontend: `frontend/server.js` → `const PORT`

### DLL Errors (Windows)
See `SETUP_WINDOWS.md` for solutions to common Windows DLL issues.

### API Key Issues
- Make sure `.env` file exists
- Check that `HF_API_KEY` is set correctly
- Verify your API key is valid at https://huggingface.co/settings/tokens

---

**Happy coding! 🚀**

