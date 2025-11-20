@echo off
REM Push project to GitHub
echo ========================================
echo Pushing to GitHub
echo ========================================
echo.

REM Check if git is initialized
git status >nul 2>&1
if errorlevel 1 (
    echo Error: Not a git repository
    echo Please run: git init
    pause
    exit /b 1
)

REM Check remote
git remote -v | findstr "origin" >nul
if errorlevel 1 (
    echo Adding remote origin...
    git remote add origin https://github.com/chakradharkalle03-arch/MCP2.git
)

REM Set branch to main
git branch -M main >nul 2>&1

REM Check if repo exists by trying to fetch
echo Checking if repository exists on GitHub...
git ls-remote --heads origin main >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo Repository not found on GitHub!
    echo ========================================
    echo.
    echo Please create the repository first:
    echo.
    echo 1. Open your browser and go to:
    echo    https://github.com/new
    echo.
    echo 2. Fill in:
    echo    - Repository name: MCP2
    echo    - Description: MCP-based RAG system for semiconductor component search
    echo    - Visibility: Public (or Private)
    echo    - DO NOT check any boxes (no README, .gitignore, license)
    echo.
    echo 3. Click "Create repository"
    echo.
    echo 4. Then run this script again
    echo.
    echo Alternatively, press any key to open GitHub in your browser...
    pause >nul
    start https://github.com/new
    exit /b 1
)

REM Push
echo Repository found! Pushing to GitHub...
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo Push failed!
    echo ========================================
    echo.
    echo Please make sure:
    echo 1. You're authenticated with GitHub
    echo 2. You have access to the repository
    echo 3. You have push permissions
    echo.
    echo To authenticate, you may need to:
    echo - Use GitHub CLI: gh auth login
    echo - Or use a Personal Access Token
    echo.
) else (
    echo.
    echo ========================================
    echo Success! Pushed to GitHub!
    echo ========================================
    echo.
    echo Repository: https://github.com/chakradharkalle03-arch/MCP2
    echo.
)

pause

