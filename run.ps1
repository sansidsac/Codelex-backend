# Codelex Backend Startup Script
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CODELEX BACKEND - Starting API Server" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
Write-Host "📁 Working directory: $(Get-Location)" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Starting server on http://localhost:8000" -ForegroundColor Yellow
Write-Host "📚 API Docs at: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn
& ".\venv\Scripts\python.exe" -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
