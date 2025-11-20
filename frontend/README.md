# Node.js Frontend for Semiconductor Component Search

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

### 3. Access the UI

**Open in your browser:**
```
http://localhost:3000
```

## 📋 Prerequisites

- **Node.js** (v14 or higher)
- **npm** (comes with Node.js)
- **Backend running** on `http://localhost:8001`

## 🔧 Configuration

Edit `frontend/.env` to configure:

```env
PORT=3000
BACKEND_URL=http://localhost:8001
```

## 🎨 Features

- ✅ **Modern UI Design** - Beautiful dark theme interface
- ✅ **File Upload** - Drag & drop Excel files
- ✅ **Question Answering** - Interactive Q&A interface
- ✅ **Real-time Status** - Connection and collection info
- ✅ **Toast Notifications** - User feedback messages
- ✅ **Responsive Design** - Works on all devices

## 📁 Project Structure

```
frontend/
├── server.js          # Express server (proxies to backend)
├── package.json       # Node.js dependencies
├── .env               # Configuration
├── public/
│   ├── index.html     # Main UI page
│   ├── styles.css     # Beautiful styling
│   └── script.js      # Frontend logic
└── uploads/           # Temporary uploads (auto-cleaned)
```

## 🔌 API Endpoints

The frontend proxies these endpoints to the backend:

- `GET /api/health` - Health check
- `GET /api/info` - Collection information
- `POST /api/upload` - Upload Excel document
- `POST /api/ask` - Ask questions

## 🎯 Usage

1. **Make sure backend is running** on port 8001
2. **Start frontend**: `npm start`
3. **Open browser**: http://localhost:3000
4. **Upload file**: Drag & drop Excel file
5. **Ask questions**: Type question or click quick buttons
6. **View answers**: See formatted answers with context

## 🛠️ Development

```bash
# Install dependencies
npm install

# Start with auto-reload
npm run dev

# Start production
npm start
```

## 📝 Notes

- Frontend runs on port 3000
- Backend should run on port 8001
- Frontend proxies all API calls to backend
- File uploads are temporarily stored and auto-cleaned

