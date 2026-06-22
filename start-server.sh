#!/bin/bash

# Start MCP Server

echo "🚀 Starting MCP Server..."

# Find Python 3.10+ (required for MCP SDK)
PYTHON_CMD=""
for cmd in python3.13 python3.12 python3.11 python3.10; do
    if command -v $cmd &> /dev/null; then
        PYTHON_CMD=$cmd
        break
    fi
done

# Fallback to python3 if specific version not found
if [ -z "$PYTHON_CMD" ]; then
    PYTHON_CMD=python3
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ Error: Python 3.10+ is required (found $PYTHON_VERSION)"
    echo "   Please install Python 3.10 or higher"
    echo "   On macOS: brew install python@3.12"
    echo "   On Ubuntu: sudo apt install python3.12"
    exit 1
fi

echo "✅ Using Python $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if dependencies are installed
if ! python -c "import mcp" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start server
cd server
echo "✅ Starting server on http://localhost:8000"
python main.py
