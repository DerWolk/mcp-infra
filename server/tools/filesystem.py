"""Filesystem Tools for MCP Server"""
import os
import aiofiles
from pathlib import Path
from typing import Any


async def read_file(path: str) -> dict[str, Any]:
    """Read content from a file"""
    try:
        file_path = Path(path).resolve()

        if not file_path.exists():
            return {"error": f"File not found: {path}"}

        if not file_path.is_file():
            return {"error": f"Path is not a file: {path}"}

        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()

        return {
            "path": str(file_path),
            "content": content,
            "size": file_path.stat().st_size
        }
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}


async def write_file(path: str, content: str) -> dict[str, Any]:
    """Write content to a file"""
    try:
        file_path = Path(path).resolve()

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)

        return {
            "path": str(file_path),
            "success": True,
            "size": file_path.stat().st_size
        }
    except Exception as e:
        return {"error": f"Error writing file: {str(e)}"}


async def list_directory(path: str) -> dict[str, Any]:
    """List contents of a directory"""
    try:
        dir_path = Path(path).resolve()

        if not dir_path.exists():
            return {"error": f"Directory not found: {path}"}

        if not dir_path.is_dir():
            return {"error": f"Path is not a directory: {path}"}

        items = []
        for item in dir_path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None,
                "path": str(item)
            })

        return {
            "path": str(dir_path),
            "items": items,
            "count": len(items)
        }
    except Exception as e:
        return {"error": f"Error listing directory: {str(e)}"}
