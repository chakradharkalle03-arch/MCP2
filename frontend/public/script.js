// Frontend JavaScript - Connects to Node.js backend which proxies to FastAPI

const API_BASE = '/api';

// DOM Elements
const statusBadge = document.getElementById('statusBadge');
const statusText = document.getElementById('statusText');
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const uploadStatus = document.getElementById('uploadStatus');
const uploadResult = document.getElementById('uploadResult');
const questionInput = document.getElementById('questionInput');
const askButton = document.getElementById('askButton');
const answerSection = document.getElementById('answerSection');
const answerContent = document.getElementById('answerContent');
const contextItems = document.getElementById('contextItems');
const copyButton = document.getElementById('copyButton');
const quickButtons = document.querySelectorAll('.quick-btn');
const docCount = document.getElementById('docCount');
const collectionName = document.getElementById('collectionName');
const collectionStatus = document.getElementById('collectionStatus');
const refreshInfoBtn = document.getElementById('refreshInfoBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const toastContainer = document.getElementById('toastContainer');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    loadCollectionInfo();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    // Upload area
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);

    // Question input
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            askQuestion();
        }
    });
    askButton.addEventListener('click', askQuestion);

    // Quick question buttons
    quickButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.getAttribute('data-question');
            questionInput.value = question;
            askQuestion();
        });
    });

    // Copy button
    copyButton.addEventListener('click', copyAnswer);

    // Refresh info
    refreshInfoBtn.addEventListener('click', loadCollectionInfo);
}

// Check Health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        if (response.ok) {
            statusBadge.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            statusBadge.classList.remove('connected');
            statusText.textContent = 'Disconnected';
        }
    } catch (error) {
        statusBadge.classList.remove('connected');
        statusText.textContent = 'Disconnected';
        showToast('Cannot connect to backend. Please check if the backend is running.', 'error');
    }
}

// File Upload Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
}

async function handleFileUpload(file) {
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
        showToast('Please upload an Excel file (.xlsx or .xls)', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    uploadProgress.style.display = 'block';
    uploadResult.style.display = 'none';
    uploadStatus.textContent = 'Uploading...';
    progressFill.style.width = '30%';

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        progressFill.style.width = '100%';

        if (response.ok) {
            const data = await response.json();
            uploadResult.className = 'upload-result success';
            uploadResult.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <strong>Success!</strong> ${data.message || 'File uploaded successfully'}
                <br><small>Processed ${data.chunks_processed || 0} chunks</small>
            `;
            uploadResult.style.display = 'block';
            uploadStatus.textContent = 'Upload complete!';
            showToast('File uploaded successfully!', 'success');
            
            // Reload collection info
            setTimeout(() => {
                loadCollectionInfo();
                uploadProgress.style.display = 'none';
            }, 2000);
        } else {
            const errorData = await response.json();
            uploadResult.className = 'upload-result error';
            uploadResult.innerHTML = `
                <i class="fas fa-exclamation-circle"></i>
                <strong>Error:</strong> ${errorData.message || errorData.error || 'Upload failed'}
            `;
            uploadResult.style.display = 'block';
            uploadStatus.textContent = 'Upload failed';
            showToast('Upload failed. Please try again.', 'error');
            uploadProgress.style.display = 'none';
        }
    } catch (error) {
        uploadResult.className = 'upload-result error';
        uploadResult.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <strong>Error:</strong> ${error.message}
        `;
        uploadResult.style.display = 'block';
        uploadStatus.textContent = 'Upload failed';
        showToast('Upload failed. Please check your connection.', 'error');
        uploadProgress.style.display = 'none';
    }
}

// Ask Question
async function askQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) {
        showToast('Please enter a question', 'error');
        return;
    }

    askButton.disabled = true;
    askButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Asking...';
    answerSection.style.display = 'none';
    showLoading();

    try {
        const response = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                n_results: 5
            })
        });

        if (response.ok) {
            const data = await response.json();
            
            // Display answer
            answerContent.innerHTML = formatAnswer(data.answer);
            
            // Display context
            if (data.context && data.context.length > 0) {
                contextItems.innerHTML = data.context.map((ctx, index) => `
                    <div class="context-item">
                        <strong>Context ${index + 1}:</strong>
                        <p>${escapeHtml(ctx.substring(0, 500))}${ctx.length > 500 ? '...' : ''}</p>
                    </div>
                `).join('');
            } else {
                contextItems.innerHTML = '<p class="context-item">No context retrieved.</p>';
            }
            
            answerSection.style.display = 'block';
            answerSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            showToast('Answer retrieved successfully!', 'success');
        } else {
            const errorData = await response.json();
            answerContent.innerHTML = `<p style="color: var(--error-color);">Error: ${errorData.message || errorData.error || 'Failed to get answer'}</p>`;
            answerSection.style.display = 'block';
            showToast('Failed to get answer. Please try again.', 'error');
        }
    } catch (error) {
        answerContent.innerHTML = `<p style="color: var(--error-color);">Error: ${error.message}</p>`;
        answerSection.style.display = 'block';
        showToast('Connection error. Please check your connection.', 'error');
    } finally {
        askButton.disabled = false;
        askButton.innerHTML = '<i class="fas fa-paper-plane"></i> Ask';
        hideLoading();
    }
}

// Format Answer
function formatAnswer(answer) {
    // Split by newlines and format
    const lines = answer.split('\n').filter(line => line.trim());
    return lines.map(line => {
        line = line.trim();
        if (line.startsWith('**') || line.match(/^[A-Z][a-z]+:/)) {
            return `<p><strong>${escapeHtml(line)}</strong></p>`;
        }
        return `<p>${escapeHtml(line)}</p>`;
    }).join('');
}

// Copy Answer
function copyAnswer() {
    const text = answerContent.innerText;
    navigator.clipboard.writeText(text).then(() => {
        copyButton.innerHTML = '<i class="fas fa-check"></i>';
        showToast('Answer copied to clipboard!', 'success');
        setTimeout(() => {
            copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        }, 2000);
    });
}

// Load Collection Info
async function loadCollectionInfo() {
    try {
        const response = await fetch(`${API_BASE}/info`);
        if (response.ok) {
            const data = await response.json();
            docCount.textContent = data.document_count || 0;
            collectionName.textContent = data.collection_name || 'N/A';
            collectionStatus.textContent = data.status || 'Unknown';
        }
    } catch (error) {
        console.error('Failed to load collection info:', error);
    }
}

// Utility Functions
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

