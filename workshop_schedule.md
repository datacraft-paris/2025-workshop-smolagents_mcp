# Workshop Schedule

## [Text to SQL Agent](./src/workshop_smolagents_mcp/text_to_sql.ipynb)

Follow the instructions in the notebook to create a text to SQL agent.

## [Web Search Agent](./src/workshop_smolagents_mcp/web_search.ipynb)

Follow the instructions in the notebook to create a web search agent.

## [Multi-Agent](./src/workshop_smolagents_mcp/multi_agent.ipynb)

Follow the instructions in the notebook to create a multi-agent system.

## [Build a FastMCP server](./src/workshop_smolagents_mcp/server.py)

Go to [event.py](./src/workshop_smolagents_mcp/event.py) and fill the TODOs

Go to [server.py](./src/workshop_smolagents_mcp/server.py) and fill the TODOs

Once done, you can open a MCP-compatible GenAI interface and register the MCP server.

For claude users: go to Settings > Developer > Edit config

For cursor users: CMD + Shift + P > View: Open MCP Settings > New MCP Server

Use the following config:

```json
{
  "mcpServers": {
    "your-mcp-server-name": {
      "command": "/path/to/your/uv/executable",
      "args": [
        "--directory",
        "/path/to/your/workshop-smolagents-mcp/src/workshop_smolagents_mcp",
        "run",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

Then, try to use it inside claude or cursor asking a relevant question.

## [Convert a FastAPI server to a FastMCP server](./src/workshop_smolagents_mcp/app.py)

Go to [app.py](./src/workshop_smolagents_mcp/app.py) and fill the TODOs

Add the following config to your MCP settings:

```json
{
  "mcpServers": {
    "your-mcp-server-name": {
      "command": "/path/to/your/uv/executable",
      "args": [
        "--directory",
        "/path/to/your/workshop-smolagents-mcp/src/workshop_smolagents_mcp",
        "run",
        "server.py"
      ],
      "env": {}
    },
    "from-fastapi": {
      "command": "/path/to/your/uv/executable",
      "args": [
        "--directory",
        "/path/to/your/workshop-smolagents-mcp/src/workshop_smolagents_mcp",
        "run",
        "app.py"
      ],
      "env": {}
    }
  }
}
```

Then, try to use it inside claude or cursor asking a relevant question.
