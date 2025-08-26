# MCP introduction

## What is an MCP server?

MCP is the "Model Context Protocol", e.g. the way for an agent to connect with tools. The MCP server is a shared, central layer to be linked by several agents and tools.

The main reason why MCP exists is for us to avoid re-inventing the wheel when it comes to tooling. There might be a thousand engineers in the world that would write the same tool, but we can just use the one that is already there.

In practice, MCP servers are the one and only point of connection between agents and tools for working at scale.

For instance, a company might have a company-wide MCP server, exposing relevant tools to each engineering team, to avoid each of these teams having to write their own tools and duplicating the effort.

Practically speaking, the MCP server can be hosted locally on your laptop (we will do that today), but it can also be hosted on a remote server, or even on a cloud provider.

### MCP Resources and Prompts

We will not see that today but MCP Servers do not only expose tools, they can also expose custom resources (e.g. data) and pre-built prompts.

### Tools

MCP Servers can hold user tools, this is what we are going to focus on today.

### MCP Client

As in every Server-Client architecture, the MCP Client is the one that will connect to the MCP Server and use its tools.

The MCP Client allow you to customize user experience while interacting with the MCP Server with the LLM.

### Control Flow

MCPs are designed to be used in a loop, with the agent using the tools to advance one step further.

In the MCP development kit, you also have access to a lot of utilities to help you build a nice user experience:
- you can ask permission to the user before using a sensitive tool, make the user validate tool usage knowing the input (e.g. email sending)
- you can display tool usage progress bar, to better communicate with the user
- you can stop execution of a tool at any point in the code to ask the user for more information and create exit or improve tools.

## MCP interfaces

As of today, there are mostly two MCP interfaces:

- Cursor -> great MCP integration
- Claude -> pioneering MCP development

Both services allow you to interact with locally-hosted MCP Servers.

In contrast, OpenAI does not have this capabilities as of now with ChatGPT, they only allow you to interact with remote-hosted MCP Servers.

## MCP Libraries

There are two main MCP libraries in Python:

- `fastmcp`, developed by an individual currently building a startup around it (think FastAPI Cloud but for MCP)
- `mcp`, which is a fork of `fastmcp`, conducted by Anthropic.

We have a slight preference for `fastmcp`, because it holds more feature at the moment.

Keep in mind that both libraries are very close to each other, and it's always possible to switch from one to the other.