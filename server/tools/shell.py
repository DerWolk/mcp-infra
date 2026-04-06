"""Shell Tools for MCP Server"""
import asyncio
from typing import Any


async def execute_shell_command(command: str, timeout: int = 30) -> dict[str, Any]:
    """Execute a shell command"""
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout
        )

        return {
            "command": command,
            "return_code": process.returncode,
            "stdout": stdout.decode('utf-8', errors='replace'),
            "stderr": stderr.decode('utf-8', errors='replace'),
            "success": process.returncode == 0
        }
    except asyncio.TimeoutError:
        return {"error": f"Command timed out after {timeout} seconds"}
    except Exception as e:
        return {"error": f"Error executing command: {str(e)}"}
