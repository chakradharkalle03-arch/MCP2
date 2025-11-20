# Windows Setup Guide

## DLL Issues on Windows

If you encounter DLL errors like:
```
OSError: [WinError 1114] A dynamic link library (DLL) initialization routine failed
```

This is a common Windows issue with PyTorch. Here are solutions:

### Solution 1: Install Visual C++ Redistributables

Download and install:
- **Visual C++ Redistributable for Visual Studio 2015-2022**
- Both **x64** and **x86** versions

Download from: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

### Solution 2: Use Conda Environment (Recommended)

```bash
# Create conda environment
conda create -n mcp2 python=3.11
conda activate mcp2

# Install PyTorch via conda
conda install pytorch torchvision cpuonly -c pytorch

# Install other dependencies
pip install -r requirements.txt
```

### Solution 3: Use WSL (Windows Subsystem for Linux)

If DLL issues persist, consider using WSL for a Linux-like environment.

### Solution 4: Check Python Environment Conflicts

Make sure you're not mixing conda and pip installations. Use one package manager consistently.

## After Fixing DLL Issues

1. Activate virtual environment:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. Verify imports:
   ```bash
   python -c "from rag_pipeline import RAGPipeline; print('OK')"
   ```

3. Start server:
   ```bash
   python main.py
   ```

## Alternative: Use Docker

If DLL issues persist, consider using Docker:

```bash
docker build -t mcp2-rag .
docker run -p 8000:8000 mcp2-rag
```

