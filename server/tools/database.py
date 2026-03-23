"""Database Tools for MCP Server"""
import aiosqlite
from typing import Any


async def query_sqlite(db_path: str, query: str) -> dict[str, Any]:
    """Execute a SELECT query on SQLite database"""
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute(query) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description] if cursor.description else []

                return {
                    "columns": columns,
                    "rows": rows,
                    "count": len(rows)
                }
    except Exception as e:
        return {"error": f"Error querying database: {str(e)}"}


async def execute_sql(db_path: str, query: str) -> dict[str, Any]:
    """Execute an INSERT/UPDATE/DELETE query on SQLite database"""
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute(query)
            await db.commit()

            return {
                "success": True,
                "message": "Query executed successfully"
            }
    except Exception as e:
        return {"error": f"Error executing SQL: {str(e)}"}


async def list_tables(db_path: str) -> dict[str, Any]:
    """List all tables in SQLite database"""
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ) as cursor:
                tables = await cursor.fetchall()

                return {
                    "tables": [table[0] for table in tables],
                    "count": len(tables)
                }
    except Exception as e:
        return {"error": f"Error listing tables: {str(e)}"}
