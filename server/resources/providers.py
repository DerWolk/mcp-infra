"""Resource Providers for MCP Server"""
from pathlib import Path
from typing import Any
import aiosqlite
import aiofiles


class FileResourceProvider:
    """Provides file resources"""

    @staticmethod
    async def get_file_resource(uri: str) -> dict[str, Any]:
        """Get file content as a resource"""
        try:
            # Parse file:// URI
            path = uri.replace("file://", "")
            file_path = Path(path).resolve()

            if not file_path.exists():
                return {"error": f"File not found: {path}"}

            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()

            return {
                "uri": uri,
                "mimeType": "text/plain",
                "text": content
            }
        except Exception as e:
            return {"error": f"Error reading file resource: {str(e)}"}

    @staticmethod
    async def list_file_resources(base_path: str = ".") -> list[str]:
        """List available file resources"""
        try:
            path = Path(base_path).resolve()
            files = []

            for file_path in path.rglob("*"):
                if file_path.is_file():
                    files.append(f"file://{file_path}")

            return files
        except Exception as e:
            return []


class DatabaseResourceProvider:
    """Provides database table resources"""

    @staticmethod
    async def get_table_resource(uri: str) -> dict[str, Any]:
        """Get database table as a resource"""
        try:
            # Parse db://path/to/db.sqlite/table_name URI
            parts = uri.replace("db://", "").split("/")
            db_path = "/".join(parts[:-1])
            table_name = parts[-1]

            async with aiosqlite.connect(db_path) as db:
                async with db.execute(f"SELECT * FROM {table_name}") as cursor:
                    rows = await cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]

                    # Format as text table
                    text = f"Table: {table_name}\n"
                    text += " | ".join(columns) + "\n"
                    text += "-" * (len(text) - 1) + "\n"

                    for row in rows:
                        text += " | ".join(str(val) for val in row) + "\n"

                    return {
                        "uri": uri,
                        "mimeType": "text/plain",
                        "text": text
                    }
        except Exception as e:
            return {"error": f"Error reading database resource: {str(e)}"}

    @staticmethod
    async def list_table_resources(db_path: str) -> list[str]:
        """List available table resources"""
        try:
            async with aiosqlite.connect(db_path) as db:
                async with db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ) as cursor:
                    tables = await cursor.fetchall()
                    return [f"db://{db_path}/{table[0]}" for table in tables]
        except Exception as e:
            return []


class SystemResourceProvider:
    """Provides system information resources"""

    @staticmethod
    async def get_system_resource(uri: str) -> dict[str, Any]:
        """Get system information as a resource"""
        import psutil
        import platform

        try:
            resource_type = uri.replace("system://", "")

            if resource_type == "info":
                text = f"""System Information
Platform: {platform.system()}
Release: {platform.release()}
Architecture: {platform.machine()}
CPU Count: {psutil.cpu_count()}
Memory Total: {psutil.virtual_memory().total / (1024**3):.2f} GB
"""
                return {
                    "uri": uri,
                    "mimeType": "text/plain",
                    "text": text
                }
            else:
                return {"error": f"Unknown system resource: {resource_type}"}
        except Exception as e:
            return {"error": f"Error reading system resource: {str(e)}"}

    @staticmethod
    async def list_system_resources() -> list[str]:
        """List available system resources"""
        return ["system://info"]
