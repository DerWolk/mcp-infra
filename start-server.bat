@echo off
REM Start MCP Server (Windows)

echo Starting MCP Server...

REM Check Python version (requires Python 3.10+)
python --version 2>&1 | findstr /R "3\.1[0-9]\." >nul
if errorlevel 1 (
    echo Error: Python 3.10+ is required for MCP SDK
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Start server
cd server
echo Starting server on http://localhost:8000
python main.py
