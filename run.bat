@echo off
echo ============================================================
echo   CODELEX BACKEND - Starting API Server
echo ============================================================
echo.

cd /d "%~dp0"
echo Working directory: %CD%
echo.

echo Starting server on http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

venv\Scripts\python.exe -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
