# 🚀 Start Both Servers - Quick Guide

## ✅ Node.js Frontend Created and Ready!

## 📋 Start Both Servers

### Option 1: Two Terminals (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd C:\Users\user\Downloads\MCP2
.\venv\Scripts\Activate.ps1
python main.py
```
Backend will run on: `http://localhost:8001`

**Terminal 2 - Start Frontend:**
```bash
cd C:\Users\user\Downloads\MCP2\frontend
npm start
```
Frontend will run on: `http://localhost:3000`

### Option 2: Batch Script (Windows)

Create `start_all.bat`:
```batch
@echo off
start "Backend" cmd /k "cd C:\Users\user\Downloads\MCP2 && .\venv\Scripts\python.exe main.py"
timeout /t 3
start "Frontend" cmd /k "cd C:\Users\user\Downloads\MCP2\frontend && npm start"
```

## 🌐 Access the UI

**Open in your browser:**
```
http://localhost:3000
```

## ✅ Verify Both Servers

**Backend Status:**
```
http://localhost:8001/health
```

**Frontend Status:**
```
http://localhost:3000/api/health
```

Both should return: `{"status": "healthy"}`

## 📊 Architecture

```
Browser (http://localhost:3000)
    ↓
Node.js/Express Frontend (Port 3000)
    ↓ Proxies API calls
FastAPI Backend (Port 8001)
    ↓
ChromaDB + RAG Pipeline
```

## 🎯 Quick Start

1. **Start Backend**:
   ```bash
   python main.py
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm start
   ```

3. **Open Browser**: http://localhost:3000

4. **Upload File**: Drag & drop Excel file

5. **Ask Questions**: Type question or click quick buttons

6. **View Answers**: See formatted answers with context

## ✅ Status

- ✅ **Backend**: Running on port 8001
- ✅ **Frontend**: Running on port 3000
- ✅ **UI**: Beautiful modern interface
- ✅ **Integration**: Fully connected

## 🚀 Ready!

**Open**: http://localhost:3000

**Enjoy the Node.js frontend!** 🎉

