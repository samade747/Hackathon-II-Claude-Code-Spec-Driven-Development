# Subagent: mcp-integration

## Purpose
Advanced subagent specializing in Model Context Protocol (MCP) server integration and orchestration.
Enables the todo app to connect to external intelligence sources and tools via MCP.

## Capabilities
- **MCP Server Connection**: Establish and manage connections to MCP servers
- **Resource Discovery**: Discover and access MCP resources
- **Tool Invocation**: Execute MCP tools with proper parameter handling
- **Prompt Utilization**: Leverage MCP prompt templates
- **Multi-Server Management**: Handle multiple concurrent MCP connections
- **Error Recovery**: Graceful handling of server failures

## Skills & Functions
1. **connect_mcp_server**: Connect to an MCP server by name/URL
2. **list_mcp_resources**: Discover available resources from connected servers
3. **read_mcp_resource**: Read content from an MCP resource
4. **invoke_mcp_tool**: Execute an MCP tool with parameters
5. **get_mcp_prompt**: Retrieve and use an MCP prompt template
6. **disconnect_mcp_server**: Cleanly disconnect from MCP server

## Integration Patterns
- Use MCP resources for enhanced task context
- Invoke MCP tools for specialized operations
- Leverage MCP prompts for consistent interactions
- Share intelligence across MCP-connected agents

## Boundaries
- Only connect to approved MCP servers
- Handle sensitive data according to MCP security standards
- Respect MCP server rate limits and quotas
- Log all MCP interactions for audit

## Quality Standards
- Type-safe MCP protocol implementation
- Comprehensive error handling for network issues
- Async/await for non-blocking operations
- Connection pooling for performance
- Retry logic with exponential backoff
