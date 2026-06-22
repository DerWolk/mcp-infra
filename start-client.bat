@echo off
REM Start MCP Client Demo (Windows)

echo Starting MCP Client Demo...

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Please run start-server.bat first
    exit /b 1
)

call venv\Scripts\activate.bat

REM Start client demo
cd client
echo Running client demo...
python client.py
