#!/usr/bin/env python3
"""
MCP Server with SSE Transport (Starlette-based)
Provides Tools, Resources, and Prompts via the Model Context Protocol
"""
import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response
from sse_starlette import EventSourceResponse

import mcp.types as types
from mcp.server import Server
from mcp.server.sse import SseServerTransport

# Import tools
from tools.filesystem import read_file, write_file, list_directory
from tools.database import query_sqlite, execute_sql, list_tables
from tools.web import fetch_url, http_request
from tools.system import get_system_info, list_processes
from tools.shell import execute_shell_command

# Import resources
from resources.providers import (
    FileResourceProvider,
    DatabaseResourceProvider,
    SystemResourceProvider
)

# Import prompts
from prompts.templates import PromptTemplates


# Create MCP server instance
mcp_server = Server("mcp-infrastructure-server")


# ============================================================================
# TOOLS REGISTRATION
# ============================================================================

@mcp_server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available tools"""
    return [
        types.Tool(
            name="read_file",
            description="Read content from a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "Content to write to the file"}
                },
                "required": ["path", "content"]
            }
        ),
        types.Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the directory to list"}
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="query_sqlite",
            description="Execute a SELECT query on SQLite database",
            inputSchema={
                "type": "object",
                "properties": {
                    "db_path": {"type": "string", "description": "Path to the SQLite database file"},
                    "query": {"type": "string", "description": "SQL SELECT query to execute"}
                },
                "required": ["db_path", "query"]
            }
        ),
        types.Tool(
            name="execute_sql",
            description="Execute INSERT/UPDATE/DELETE query on SQLite database",
            inputSchema={
                "type": "object",
                "properties": {
                    "db_path": {"type": "string", "description": "Path to the SQLite database file"},
                    "query": {"type": "string", "description": "SQL query to execute"}
                },
                "required": ["db_path", "query"]
            }
        ),
        types.Tool(
            name="list_tables",
            description="List all tables in SQLite database",
            inputSchema={
                "type": "object",
                "properties": {
                    "db_path": {"type": "string", "description": "Path to the SQLite database file"}
                },
                "required": ["db_path"]
            }
        ),
        types.Tool(
            name="fetch_url",
            description="Fetch content from a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to fetch"},
                    "method": {"type": "string", "description": "HTTP method (GET, POST, etc.)", "default": "GET"}
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="http_request",
            description="Make an HTTP request with custom headers and body",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to request"},
                    "method": {"type": "string", "description": "HTTP method", "default": "GET"},
                    "headers": {"type": "object", "description": "HTTP headers"},
                    "body": {"type": "string", "description": "Request body"}
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="get_system_info",
            description="Get system information (CPU, memory, disk)",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="list_processes",
            description="List running processes",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="execute_shell_command",
            description="Execute a shell command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"},
                    "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30}
                },
                "required": ["command"]
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[types.TextContent]:
    """Handle tool calls"""
    result = None

    if name == "read_file":
        result = await read_file(arguments["path"])
    elif name == "write_file":
        result = await write_file(arguments["path"], arguments["content"])
    elif name == "list_directory":
        result = await list_directory(arguments["path"])
    elif name == "query_sqlite":
        result = await query_sqlite(arguments["db_path"], arguments["query"])
    elif name == "execute_sql":
        result = await execute_sql(arguments["db_path"], arguments["query"])
    elif name == "list_tables":
        result = await list_tables(arguments["db_path"])
    elif name == "fetch_url":
        result = await fetch_url(arguments["url"], arguments.get("method", "GET"))
    elif name == "http_request":
        result = await http_request(
            arguments["url"],
            arguments.get("method", "GET"),
            arguments.get("headers"),
            arguments.get("body")
        )
    elif name == "get_system_info":
        result = await get_system_info()
    elif name == "list_processes":
        result = await list_processes()
    elif name == "execute_shell_command":
        result = await execute_shell_command(arguments["command"], arguments.get("timeout", 30))
    else:
        result = {"error": f"Unknown tool: {name}"}

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


# ============================================================================
# RESOURCES REGISTRATION
# ============================================================================

@mcp_server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List all available resources"""
    return [
        types.Resource(
            uri="file://README.md",
            name="README",
            mimeType="text/plain",
            description="Project README file"
        ),
        types.Resource(
            uri="system://info",
            name="System Information",
            mimeType="text/plain",
            description="Current system information"
        )
    ]


@mcp_server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI"""
    uri_str = str(uri)

    if uri_str.startswith("file://"):
        result = await FileResourceProvider.get_file_resource(uri_str)
    elif uri_str.startswith("db://"):
        result = await DatabaseResourceProvider.get_table_resource(uri_str)
    elif uri_str.startswith("system://"):
        result = await SystemResourceProvider.get_system_resource(uri_str)
    else:
        return json.dumps({"error": f"Unknown resource URI scheme: {uri_str}"})

    if "error" in result:
        return json.dumps(result)

    return result.get("text", json.dumps(result))


# ============================================================================
# PROMPTS REGISTRATION
# ============================================================================

@mcp_server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    """List all available prompts"""
    templates = PromptTemplates.list_all_prompts()
    prompts = []

    for template in templates:
        prompts.append(
            types.Prompt(
                name=template["name"],
                description=template["description"],
                arguments=[
                    types.PromptArgument(
                        name=arg["name"],
                        description=arg["description"],
                        required=arg["required"]
                    )
                    for arg in template["arguments"]
                ]
            )
        )

    return prompts


@mcp_server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Get a prompt by name"""
    templates = {
        "code_review": PromptTemplates.get_code_review_prompt,
        "sql_helper": PromptTemplates.get_sql_helper_prompt,
        "system_diagnostics": PromptTemplates.get_system_diagnostics_prompt,
        "api_integration": PromptTemplates.get_api_integration_prompt
    }

    if name not in templates:
        raise ValueError(f"Unknown prompt: {name}")

    template = templates[name]()
    prompt_text = template["prompt"]

    if arguments:
        for key, value in arguments.items():
            prompt_text = prompt_text.replace(f"{{{{{key}}}}}", value)

    return types.GetPromptResult(
        description=template["description"],
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_text)
            )
        ]
    )


# ============================================================================
# SSE ENDPOINTS
# ============================================================================

# Store active SSE sessions
sse_sessions = {}


async def handle_sse(request: Request):
    """Handle SSE connections"""
    async def event_generator():
        # Create SSE transport for this connection
        async with SseServerTransport("/message") as transport:
            # Store session
            session_id = id(transport)
            sse_sessions[session_id] = transport

            try:
                # Run the MCP server
                async with asyncio.TaskGroup() as tg:
                    # Start server
                    tg.create_task(
                        mcp_server.run(
                            transport.read_stream,
                            transport.write_stream,
                            mcp_server.create_initialization_options()
                        )
                    )

                    # Send events
                    async for message in transport.read_stream:
                        if message:
                            yield {
                                "event": "message",
                                "data": json.dumps(message)
                            }
            finally:
                # Cleanup
                sse_sessions.pop(session_id, None)

    return EventSourceResponse(event_generator())


async def handle_message(request: Request):
    """Handle POST messages"""
    data = await request.json()

    # This would route to the appropriate SSE session
    # For now, return acknowledgment
    return Response(
        content=json.dumps({"status": "received"}),
        media_type="application/json"
    )


async def handle_health(request: Request):
    """Health check endpoint"""
    return Response(
        content=json.dumps({
            "status": "healthy",
            "server": "mcp-infrastructure-server",
            "transport": "sse",
            "active_sessions": len(sse_sessions)
        }),
        media_type="application/json"
    )


# ============================================================================
# STARLETTE APP
# ============================================================================

@asynccontextmanager
async def lifespan(app):
    """Application lifespan"""
    print("🚀 MCP Server (SSE) starting...")
    yield
    print("👋 MCP Server (SSE) shutting down...")


app = Starlette(
    debug=True,
    routes=[
        Route("/sse", handle_sse),
        Route("/message", handle_message, methods=["POST"]),
        Route("/health", handle_health),
    ],
    lifespan=lifespan
)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting MCP Server with SSE Transport")
    print("📡 SSE endpoint: http://localhost:8000/sse")
    print("📬 Message endpoint: http://localhost:8000/message")
    print("❤️  Health check: http://localhost:8000/health")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
