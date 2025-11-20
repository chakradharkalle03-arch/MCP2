# 🚀 Node.js Frontend - Complete Guide

## ✨ Node.js Frontend Created!

A beautiful Node.js/Express frontend has been created that connects to your FastAPI backend!

## 📋 Architecture

```
Browser (Port 3000)
    ↓
Node.js/Express Frontend
    ↓
FastAPI Backend (Port 8001)
    ↓
ChromaDB + RAG Pipeline
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Frontend Server

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

### 3. Make Sure Backend is Running

In another terminal:

```bash
cd ..  # Go back to project root
python main.py
```

### 4. Access the UI

**Open in your browser:**
```
http://localhost:3000
```

## 🎨 Features

### Frontend Features
- ✅ **Node.js/Express Server** - Proxy to backend
- ✅ **Beautiful UI** - Modern dark theme design
- ✅ **File Upload** - Drag & drop Excel files
- ✅ **Question Answering** - Interactive Q&A interface
- ✅ **Real-time Status** - Connection indicators
- ✅ **Toast Notifications** - User feedback
- ✅ **Responsive Design** - Works on all devices

### Backend Integration
- ✅ **Health Check** - Proxies `/api/health` to backend
- ✅ **Collection Info** - Proxies `/api/info` to backend
- ✅ **File Upload** - Proxies `/api/upload` to backend
- ✅ **Question Answering** - Proxies `/api/ask` to backend

## 📁 Project Structure

```
frontend/
├── server.js              # Express server (proxy)
├── package.json           # Node.js dependencies
├── .env                   # Configuration
├── README.md              # Frontend documentation
├── .gitignore            # Git ignore rules
├── public/               # Static files
│   ├── index.html        # Main UI page
│   ├── styles.css        # Beautiful styling
│   └── script.js         # Frontend logic
└── uploads/              # Temporary uploads (auto-cleaned)
```

## 🔧 Configuration

Edit `frontend/.env`:

```env
PORT=3000
BACKEND_URL=http://localhost:8001
```

## 🎯 Usage

### Start Both Servers

**Terminal 1 (Backend):**
```bash
cd C:\Users\user\Downloads\MCP2
.\venv\Scripts\python.exe main.py
```

**Terminal 2 (Frontend):**
```bash
cd C:\Users\user\Downloads\MCP2\frontend
npm start
```

### Access the UI

1. **Open browser**: http://localhost:3000
2. **Upload file**: Drag & drop Excel file
3. **Ask questions**: Type question or click quick buttons
4. **View answers**: See formatted answers with context

## 📊 API Endpoints

The frontend proxies these to the backend:

| Frontend Endpoint | Backend Endpoint | Method | Description |
|-------------------|------------------|--------|-------------|
| `/api/health` | `/health` | GET | Health check |
| `/api/info` | `/info` | GET | Collection info |
| `/api/upload` | `/upload` | POST | Upload Excel |
| `/api/ask` | `/ask` | POST | Ask questions |

## 🎨 UI Features

- **Drag & Drop Upload** - Easy file upload
- **Quick Question Buttons** - Pre-defined questions
- **Formatted Answers** - Clean answer display
- **Context Visualization** - Retrieved context shown
- **Copy to Clipboard** - Easy answer copying
- **Status Indicators** - Connection status
- **Toast Notifications** - User feedback
- **Loading Overlays** - Visual feedback

## 💡 Example Usage

1. **Open**: http://localhost:3000
2. **Upload**: Drag `examples/semiconductor_components.xlsx` to upload area
3. **Ask**: Click "MOSFET" quick button or type your question
4. **View**: See formatted answer with context
5. **Copy**: Click copy button to copy answer

## 🔧 Development

```bash
# Install dependencies
cd frontend
npm install

# Start with auto-reload (requires nodemon)
npm run dev

# Start production
npm start
```

## 📝 Dependencies

- **express**: Web server
- **axios**: HTTP client for backend communication
- **multer**: File upload handling
- **cors**: CORS middleware
- **dotenv**: Environment variables
- **nodemon** (dev): Auto-reload for development

## ✅ Status

**Frontend**: Node.js/Express server  
**Backend**: FastAPI server on port 8001  
**UI**: Beautiful modern interface  
**Integration**: Fully connected  

## 🚀 Ready!

**Start frontend**: `cd frontend && npm start`  
**Access UI**: http://localhost:3000  
**Make sure backend is running**: `python main.py`

**Enjoy the beautiful Node.js frontend!** 🎉

