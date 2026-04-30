#!/usr/bin/env python3
"""
MCP Client with SSE Transport
Connects to MCP Server and demonstrates tool/resource/prompt usage
"""
import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client


class MCPClient:
    """MCP Client for interacting with the server"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session: ClientSession | None = None

    async def connect(self):
        """Connect to the MCP server"""
        print(f"🔌 Connecting to MCP server at {self.base_url}...")

        # Create SSE client
        async with sse_client(f"{self.base_url}/sse") as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session

                # Initialize the session
                await session.initialize()

                print("✅ Connected to MCP server")
                return session

    async def list_tools(self):
        """List all available tools"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        tools = await self.session.list_tools()
        print(f"\n📦 Available Tools ({len(tools.tools)}):")
        for tool in tools.tools:
            print(f"  • {tool.name}: {tool.description}")

        return tools.tools

    async def list_resources(self):
        """List all available resources"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        resources = await self.session.list_resources()
        print(f"\n📚 Available Resources ({len(resources.resources)}):")
        for resource in resources.resources:
            print(f"  • {resource.name} ({resource.uri}): {resource.description}")

        return resources.resources

    async def list_prompts(self):
        """List all available prompts"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        prompts = await self.session.list_prompts()
        print(f"\n💬 Available Prompts ({len(prompts.prompts)}):")
        for prompt in prompts.prompts:
            print(f"  • {prompt.name}: {prompt.description}")

        return prompts.prompts

    async def call_tool(self, name: str, arguments: dict):
        """Call a tool"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        print(f"\n🔧 Calling tool: {name}")
        print(f"   Arguments: {json.dumps(arguments, indent=2)}")

        result = await self.session.call_tool(name, arguments)

        print(f"   Result:")
        for content in result.content:
            if hasattr(content, 'text'):
                print(f"   {content.text}")

        return result

    async def read_resource(self, uri: str):
        """Read a resource"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        print(f"\n📖 Reading resource: {uri}")

        result = await self.session.read_resource(uri)

        print(f"   Content:")
        for content in result.contents:
            if hasattr(content, 'text'):
                print(f"   {content.text[:200]}...")  # First 200 chars

        return result

    async def get_prompt(self, name: str, arguments: dict | None = None):
        """Get a prompt"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        print(f"\n💭 Getting prompt: {name}")
        if arguments:
            print(f"   Arguments: {json.dumps(arguments, indent=2)}")

        result = await self.session.get_prompt(name, arguments)

        print(f"   Description: {result.description}")
        print(f"   Messages:")
        for message in result.messages:
            print(f"     Role: {message.role}")
            if hasattr(message.content, 'text'):
                print(f"     Content: {message.content.text[:200]}...")

        return result


async def demo():
    """Demo the MCP client capabilities"""
    client = MCPClient()

    try:
        async with sse_client("http://localhost:8000/sse") as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                print("✅ Connected to MCP server\n")

                # List available capabilities
                print("=" * 60)
                tools = await session.list_tools()
                print(f"\n📦 Available Tools ({len(tools.tools)}):")
                for tool in tools.tools:
                    print(f"  • {tool.name}: {tool.description}")

                print("\n" + "=" * 60)
                resources = await session.list_resources()
                print(f"\n📚 Available Resources ({len(resources.resources)}):")
                for resource in resources.resources:
                    print(f"  • {resource.name} ({resource.uri})")

                print("\n" + "=" * 60)
                prompts = await session.list_prompts()
                print(f"\n💬 Available Prompts ({len(prompts.prompts)}):")
                for prompt in prompts.prompts:
                    print(f"  • {prompt.name}: {prompt.description}")

                # Demo: Call a tool
                print("\n" + "=" * 60)
                print("\n🔧 DEMO: Calling 'get_system_info' tool")
                result = await session.call_tool("get_system_info", {})
                for content in result.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        print(f"\nSystem Info:")
                        print(f"  Platform: {data.get('platform')}")
                        print(f"  CPU Count: {data.get('cpu_count')}")
                        print(f"  Memory: {data.get('memory', {}).get('percent')}% used")

                # Demo: Read a resource
                print("\n" + "=" * 60)
                print("\n📖 DEMO: Reading 'system://info' resource")
                result = await session.read_resource("system://info")
                for content in result.contents:
                    if hasattr(content, 'text'):
                        print(f"\n{content.text}")

                # Demo: Get a prompt
                print("\n" + "=" * 60)
                print("\n💭 DEMO: Getting 'code_review' prompt")
                result = await session.get_prompt(
                    "code_review",
                    {"code": "def hello(): print('world')"}
                )
                print(f"\nPrompt Description: {result.description}")
                for message in result.messages:
                    if hasattr(message.content, 'text'):
                        print(f"\nPrompt Text:\n{message.content.text[:300]}...")

                print("\n" + "=" * 60)
                print("\n✅ Demo completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 MCP Client Demo\n")
    asyncio.run(demo())
