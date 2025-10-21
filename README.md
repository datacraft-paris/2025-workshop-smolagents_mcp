<p align="center">
  <img src="assets/datacraft_logo.svg" alt="Logo" width="337"/>
</p>
<br/>

# 2025 - Workshop – Building AI Agents and MCP servers

Welcome to this hands-on workshop on **Building AI Agents and MCP Servers**.
In this workshop, we will build simple AI Agents using the library `smolagents` from HuggingFace and MCP Servers using the library `fastmcp`.

Finally, we will see how a custom client can link both, letting the agent call tools from the distant MCP server. Technical terms like MCP Servers, Agents, and MCP Clients will be introduced too.

---

## Table of Contents
- **[Learning Objectives](#learning-objectives)**
- **[Workshop Structure](#workshop-structure)**
    - **[Part 1: AI Agents](#part-1-ai-agents)**
    - **[Part 2: MCP Servers](#part-2-mcp-servers)**
- **[Repository Organization](#repository-organization)**
    - **[Difficulty Levels](#difficulty-levels)**
    - **[Navigating the Workshop](#navigating-the-workshop)**

---

## Learning Objectives

After completing this workshop, you will be able to:
- Build simple AI Agents using the library `smolagents` from HuggingFace
- Build MCP Servers using the library `fastmcp`
- Build a custom client to link both, letting the agent call tools from the distant MCP server
- Convert an existing fastapi API into an MCP server that can be leveraged by an agent
- Understand the technical terms like MCP Servers, Agents, and MCP Clients

## Workshop Structure
The workshop will cover the following topics:
### **Part 1**: AI Agents
- **I**: Building a text-to-sql agent to ask questions about datacrafts' events and get an answer grounded in true data.
- **II**: Building a web search agent to get a sourced answer to a question
- **III**: Building a multi-agent system to source, analyze and summarize french AI call for projects
### **Part 2**: MCP Servers
- **I**: Integrate previously-developed tools into an MCP server using `fastmcp`
- **II**: Explore the `fastapi` scenario, where we would like to convert an existing fastapi API, containing previously-developed tools, into an MCP server

## Repository Organization

| Branch         | Purpose                                                                    |
|----------------|----------------------------------------------------------------------------|
| `main`         | Core concepts and theoretical foundations                                  |
| `easy`         | Beginner-friendly version: **fill the blanks**                             |
| `intermediate` | Intermediate version: **fill a few lines**                                 |
| `hard`         | Advanced version: **implement whole functions from docs**                  | 
| `correction`   | Complete solutions with detailed explanations                              |

**Recommendation**: Start with the `main` branch to grasp the theoretical foundations. Choose your subsequent branch based on your experience level.

### Difficulty Levels

The workshop materials are organized as follows:

- **Core Components**:
  - `src/workshop_smolagents_mcp/`: notebooks / python files containing the workshop content
  - `src/workshop_smolagents_mcp/TODO_*.md`: Detailed instructions for each python files (for notebooks, instructions are in the notebook itself)

### Navigating the Workshop

This workshop offers different difficulty levels to match your learning pace. To switch between levels:

```bash
git checkout <branch-name>
```

Replace `<branch-name>` with one of the following :

- `main`         → introduction, theory and definitions
- `easy`         → easy version
- `intermediate` → intermediate version
- `hard`         → advanced version
- `correction`   → complete solution
