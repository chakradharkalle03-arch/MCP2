"""
MCP Server for ChromaDB Integration
This demonstrates how MCP works as a protocol for context retrieval
"""
import asyncio
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import config

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=config.CHROMA_PERSIST_DIR,
    settings=Settings(anonymized_telemetry=False)
)

# Initialize MCP Server
app = Server("chromadb-mcp-server")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools for ChromaDB operations"""
    return [
        Tool(
            name="query_semiconductor_data",
            description="Query semiconductor component data from ChromaDB using semantic search. This demonstrates MCP's purpose: providing structured context retrieval through tools.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The semantic query to search for in the database"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_collection_info",
            description="Get information about the ChromaDB collection",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls from MCP clients"""
    if name == "query_semiconductor_data":
        query = arguments.get("query", "")
        n_results = arguments.get("n_results", 5)
        
        try:
            collection = chroma_client.get_or_create_collection(
                name=config.CHROMA_COLLECTION_NAME
            )
            
            # Query ChromaDB
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and len(results['documents'][0]) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                    formatted_results.append(
                        f"Document {i+1}:\n{doc}\nMetadata: {metadata}\n"
                    )
                response = "\n---\n".join(formatted_results)
            else:
                response = "No results found for the query."
            
            return [TextContent(type="text", text=response)]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Error querying ChromaDB: {str(e)}")]
    
    elif name == "get_collection_info":
        try:
            collection = chroma_client.get_or_create_collection(
                name=config.CHROMA_COLLECTION_NAME
            )
            count = collection.count()
            return [TextContent(
                type="text",
                text=f"Collection '{config.CHROMA_COLLECTION_NAME}' contains {count} documents."
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting collection info: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="chromadb-mcp-server",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())

