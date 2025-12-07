"""
MCP (Model Context Protocol) integration layer.
Enables agents to connect to MCP servers and use their resources/tools.
"""
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
import json


@dataclass
class MCPServer:
    """Represents an MCP server connection."""
    name: str
    url: str
    connected: bool = False
    resources: List[Dict[str, Any]] = field(default_factory=list)
    tools: List[Dict[str, Any]] = field(default_factory=list)
    prompts: List[Dict[str, Any]] = field(default_factory=list)


class MCPClient:
    """
    MCP client for connecting to and interacting with MCP servers.
    Follows the Model Context Protocol specification.
    """
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self._resource_handlers: Dict[str, Callable] = {}
        self._tool_handlers: Dict[str, Callable] = {}
    
    def connect_server(self, name: str, url: str) -> str:
        """
        Connect to an MCP server.
        
        Args:
            name: Server identifier
            url: Server URL or connection string
            
        Returns:
            Connection status message
        """
        try:
            # In a real implementation, this would establish WebSocket/HTTP connection
            server = MCPServer(name=name, url=url, connected=True)
            
            # Simulate resource discovery
            server.resources = [
                {"uri": f"{name}://docs/readme", "name": "README", "mimeType": "text/plain"},
                {"uri": f"{name}://data/tasks", "name": "Tasks Data", "mimeType": "application/json"}
            ]
            
            # Simulate tool discovery
            server.tools = [
                {"name": "analyze_task", "description": "Analyze task complexity", "inputSchema": {"task_id": "string"}},
                {"name": "suggest_priority", "description": "Suggest task priority", "inputSchema": {"title": "string"}}
            ]
            
            # Simulate prompt discovery
            server.prompts = [
                {"name": "task_breakdown", "description": "Break down complex task", "arguments": ["task_description"]},
                {"name": "code_review", "description": "Review code quality", "arguments": ["code_snippet"]}
            ]
            
            self.servers[name] = server
            return f"✓ Connected to MCP server '{name}' at {url}\n" \
                   f"  - {len(server.resources)} resources available\n" \
                   f"  - {len(server.tools)} tools available\n" \
                   f"  - {len(server.prompts)} prompts available"
                   
        except Exception as e:
            return f"✗ Failed to connect to MCP server '{name}': {e}"
    
    def list_resources(self, server_name: Optional[str] = None) -> str:
        """
        List available MCP resources.
        
        Args:
            server_name: Specific server (None for all)
            
        Returns:
            Formatted list of resources
        """
        if server_name:
            if server_name not in self.servers:
                return f"✗ Server '{server_name}' not connected"
            servers = {server_name: self.servers[server_name]}
        else:
            servers = self.servers
        
        if not servers:
            return "No MCP servers connected. Use connect_server() first."
        
        output = ["MCP Resources:\n"]
        for name, server in servers.items():
            output.append(f"📡 Server: {name}")
            for resource in server.resources:
                output.append(f"  - {resource['name']} ({resource['uri']})")
        
        return "\n".join(output)
    
    def read_resource(self, uri: str) -> str:
        """
        Read content from an MCP resource.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content
        """
        # Parse server from URI
        parts = uri.split("://")
        if len(parts) != 2:
            return f"✗ Invalid URI format: {uri}"
        
        server_name = parts[0]
        resource_path = parts[1]
        
        if server_name not in self.servers:
            return f"✗ Server '{server_name}' not connected"
        
        # Simulate reading resource
        if "readme" in resource_path.lower():
            return """# MCP Server Documentation
            
This is a simulated MCP resource containing documentation.
In a real implementation, this would fetch actual content from the MCP server.

## Features
- Resource discovery and access
- Tool invocation
- Prompt templates
"""
        elif "tasks" in resource_path.lower():
            return json.dumps({
                "tasks": [
                    {"id": "1", "title": "Integrate MCP", "status": "in_progress"},
                    {"id": "2", "title": "Add cloud skills", "status": "completed"}
                ]
            }, indent=2)
        
        return f"Resource content from {uri}"
    
    def invoke_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Invoke an MCP tool.
        
        Args:
            server_name: Server identifier
            tool_name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        if server_name not in self.servers:
            return f"✗ Server '{server_name}' not connected"
        
        server = self.servers[server_name]
        tool = next((t for t in server.tools if t['name'] == tool_name), None)
        
        if not tool:
            return f"✗ Tool '{tool_name}' not found on server '{server_name}'"
        
        # Simulate tool execution
        if tool_name == "analyze_task":
            task_id = arguments.get('task_id', 'unknown')
            return f"""Task Analysis for {task_id}:
- Estimated complexity: Medium
- Suggested time: 2-4 hours
- Dependencies: None
- Risks: Low
"""
        elif tool_name == "suggest_priority":
            title = arguments.get('title', '')
            if 'urgent' in title.lower() or 'critical' in title.lower():
                return "Suggested priority: HIGH"
            elif 'later' in title.lower() or 'someday' in title.lower():
                return "Suggested priority: LOW"
            return "Suggested priority: MEDIUM"
        
        return f"Tool '{tool_name}' executed with arguments: {json.dumps(arguments)}"
    
    def get_prompt(self, server_name: str, prompt_name: str, arguments: Dict[str, Any]) -> str:
        """
        Get an MCP prompt template.
        
        Args:
            server_name: Server identifier
            prompt_name: Prompt name
            arguments: Prompt arguments
            
        Returns:
            Filled prompt template
        """
        if server_name not in self.servers:
            return f"✗ Server '{server_name}' not connected"
        
        server = self.servers[server_name]
        prompt = next((p for p in server.prompts if p['name'] == prompt_name), None)
        
        if not prompt:
            return f"✗ Prompt '{prompt_name}' not found on server '{server_name}'"
        
        # Simulate prompt template filling
        if prompt_name == "task_breakdown":
            task_desc = arguments.get('task_description', '')
            return f"""Please break down the following task into subtasks:

Task: {task_desc}

Subtasks:
1. Research and planning phase
2. Implementation phase  
3. Testing phase
4. Documentation phase
5. Review and refinement

For each subtask, provide:
- Estimated time
- Required skills
- Dependencies
"""
        elif prompt_name == "code_review":
            code = arguments.get('code_snippet', '')
            return f"""Please review this code for:
- Code quality and style
- Potential bugs
- Performance issues
- Security concerns  
- Best practices

Code:
{code}
"""
        
        return f"Prompt '{prompt_name}' with arguments: {json.dumps(arguments)}"
    
    def disconnect_server(self, name: str) -> str:
        """
        Disconnect from an MCP server.
        
        Args:
            name: Server identifier
            
        Returns:
            Disconnection status
        """
        if name in self.servers:
            del self.servers[name]
            return f"✓ Disconnected from MCP server '{name}'"
        return f"✗ Server '{name}' not connected"
    
    def get_server_status(self) -> str:
        """
        Get status of all connected  MCP servers.
        
        Returns:
            Server status summary
        """
        if not self.servers:
            return "No MCP servers connected"
        
        output = ["MCP Server Status:\n"]
        for name, server in self.servers.items():
            status = "🟢 Connected" if server.connected else "🔴 Disconnected"
            output.append(f"{status} {name} ({server.url})")
            output.append(f"  Resources: {len(server.resources)}, Tools: {len(server.tools)}, Prompts: {len(server.prompts)}")
        
        return "\n".join(output)


# Global MCP client instance
mcp_client = MCPClient()


# Skill functions that can be added to agents
def connect_mcp_server(name: str, url: str) -> str:
    """Connect to an MCP server."""
    return mcp_client.connect_server(name, url)


def list_mcp_resources(server_name: Optional[str] = None) -> str:
    """List MCP resources."""
    return mcp_client.list_resources(server_name)


def read_mcp_resource(uri: str) -> str:
    """Read an MCP resource."""
    return mcp_client.read_resource(uri)


def invoke_mcp_tool(server_name: str, tool_name: str, **arguments) -> str:
    """Invoke an MCP tool."""
    return mcp_client.invoke_tool(server_name, tool_name, arguments)


def get_mcp_prompt(server_name: str, prompt_name: str, **arguments) -> str:
    """Get an MCP prompt."""
    return mcp_client.get_prompt(server_name, prompt_name, arguments)


def mcp_server_status() -> str:
    """Get MCP server status."""
    return mcp_client.get_server_status()
