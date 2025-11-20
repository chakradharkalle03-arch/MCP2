# PowerShell script to create GitHub repo and push
# Note: Requires GitHub Personal Access Token or browser authentication

Write-Host "========================================"
Write-Host "GitHub Repository Setup"
Write-Host "========================================"
Write-Host ""

Write-Host "To push to GitHub, you need to:"
Write-Host ""
Write-Host "OPTION 1: Create repository manually (Recommended)"
Write-Host "1. Go to: https://github.com/new"
Write-Host "2. Repository name: MCP2"
Write-Host "3. Description: MCP-based RAG system for semiconductor component search"
Write-Host "4. Visibility: Public (or Private)"
Write-Host "5. DO NOT check any boxes (no README, .gitignore, license)"
Write-Host "6. Click 'Create repository'"
Write-Host ""
Write-Host "Then run: git push -u origin main"
Write-Host ""
Write-Host "OPTION 2: Use GitHub CLI (if installed)"
Write-Host "gh repo create chakradharkalle03-arch/MCP2 --public --source=. --remote=origin --push"
Write-Host ""
Write-Host "Current status:"
git status --short | Select-Object -First 5
Write-Host ""
Write-Host "Ready to push! Just create the repository on GitHub first."
Write-Host ""

