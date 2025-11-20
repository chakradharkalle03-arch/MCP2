"""
Example MCP Client - Demonstrates how to use MCP for context retrieval
This shows the purpose of MCP: standardized protocol for tool-based context retrieval
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import subprocess
import sys


async def demonstrate_mcp():
    """Demonstrate MCP protocol for context retrieval"""
    print("\n" + "="*60)
    print("MCP Client Demo - Demonstrating MCP Purpose")
    print("="*60)
    
    # MCP Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize MCP session
            await session.initialize()
            
            # List available tools (MCP feature: standardized tool discovery)
            print("\n1. Discovering available MCP tools...")
            tools = await session.list_tools()
            print(f"   Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description}")
            
            # Get collection info (MCP tool call)
            print("\n2. Getting collection information via MCP...")
            result = await session.call_tool(
                "get_collection_info",
                arguments={}
            )
            print(f"   Result: {result.content[0].text}")
            
            # Query semiconductor data (MCP tool call - demonstrates context retrieval)
            print("\n3. Querying semiconductor data via MCP...")
            print("   Query: 'MOSFET components'")
            result = await session.call_tool(
                "query_semiconductor_data",
                arguments={
                    "query": "MOSFET components",
                    "n_results": 3
                }
            )
            print(f"   Retrieved context via MCP:")
            print(f"   {result.content[0].text}")
            
            # Another query
            print("\n4. Another query via MCP...")
            print("   Query: 'voltage regulator'")
            result = await session.call_tool(
                "query_semiconductor_data",
                arguments={
                    "query": "voltage regulator",
                    "n_results": 2
                }
            )
            print(f"   Retrieved context via MCP:")
            print(f"   {result.content[0].text}")
            
            print("\n" + "="*60)
            print("MCP Purpose Demonstrated:")
            print("- Standardized tool-based context retrieval")
            print("- Protocol-level abstraction for data access")
            print("- Structured communication between components")
            print("="*60 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_mcp())
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure ChromaDB has data loaded first.")
        print("Run the API and upload an Excel file to populate the database.")

