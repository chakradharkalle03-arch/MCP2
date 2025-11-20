/**
 * Node.js Express Frontend Server
 * Connects to FastAPI Backend for Semiconductor Component Search
 */
const express = require('express');
const axios = require('axios');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8001';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Configure multer for file uploads
const upload = multer({
    dest: 'uploads/',
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB limit
    },
    fileFilter: (req, file, cb) => {
        const allowedTypes = [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
            'application/vnd.ms-excel' // .xls
        ];
        if (allowedTypes.includes(file.mimetype)) {
            cb(null, true);
        } else {
            cb(new Error('Invalid file type. Please upload Excel files (.xlsx or .xls)'));
        }
    }
});

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Health check - proxy to backend
app.get('/api/health', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/health`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ 
            error: 'Backend connection failed',
            message: error.message 
        });
    }
});

// Get collection info - proxy to backend
app.get('/api/info', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/info`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to get collection info',
            message: error.message 
        });
    }
});

// Upload document - proxy to backend
app.post('/api/upload', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file provided' });
        }

        // Create FormData to forward to backend
        const FormData = require('form-data');
        const fs = require('fs');
        const formData = new FormData();
        
        formData.append('file', fs.createReadStream(req.file.path), {
            filename: req.file.originalname,
            contentType: req.file.mimetype
        });

        // Forward to backend
        const response = await axios.post(`${BACKEND_URL}/upload`, formData, {
            headers: {
                ...formData.getHeaders()
            },
            maxContentLength: Infinity,
            maxBodyLength: Infinity
        });

        // Clean up uploaded file
        fs.unlinkSync(req.file.path);

        res.json(response.data);
    } catch (error) {
        // Clean up uploaded file on error
        if (req.file && req.file.path) {
            const fs = require('fs');
            try {
                fs.unlinkSync(req.file.path);
            } catch (e) {
                console.error('Error cleaning up file:', e);
            }
        }

        res.status(error.response?.status || 500).json({
            error: 'Upload failed',
            message: error.response?.data?.detail || error.message
        });
    }
});

// Ask question - proxy to backend
app.post('/api/ask', async (req, res) => {
    try {
        const { question, n_results = 5 } = req.body;

        if (!question) {
            return res.status(400).json({ error: 'Question is required' });
        }

        const response = await axios.post(`${BACKEND_URL}/ask`, {
            question,
            n_results
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            error: 'Failed to get answer',
            message: error.response?.data?.detail || error.message
        });
    }
});

// Start server
app.listen(PORT, () => {
    console.log('\n' + '='.repeat(60));
    console.log('🚀 Frontend Server Started!');
    console.log('='.repeat(60));
    console.log(`📱 Frontend: http://localhost:${PORT}`);
    console.log(`🔌 Backend:  ${BACKEND_URL}`);
    console.log('='.repeat(60) + '\n');
});

