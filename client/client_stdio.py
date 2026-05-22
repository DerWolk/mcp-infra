#!/usr/bin/env python3
"""
MCP Client with stdio Transport
Connects to MCP Server via stdin/stdout
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Main demo function"""
    print("🚀 MCP Client Demo (stdio)\n")

    # Path to the server script
    server_script = "../server/main_stdio.py"

    # Create server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[server_script],
        env=None
    )

    try:
        async with stdio_client(server_params) as (read, write):
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
    asyncio.run(main())
