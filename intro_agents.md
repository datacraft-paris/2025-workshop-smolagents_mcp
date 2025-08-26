# Introduction to agents

## What is an AI Agent?

There is a lot of fuss about agents and their meaning nowadays. There is mostly three definitions people use nowadays:

1. **Agentic Workflow**: a workflow that is composed of multiple agents, each with a specific role and responsibility.

This is mostly prompt engineering. While this can refer to an agent in the sense that there is a persona and specialization for each sub-workflow, we decide not to use this definition today.

2. **CoT and reasoning models**: a model that can build up a reasoning chain to solve a problem.

This is also not a definition we will use today. Even if those techniques/models seem to produce an action plan, they often lack the ability to have a real impact on their environment.

3. **Tooled Agents**: a model that can use tools to solve a problem.

This is the definition we will use today. The best way to imagine it is through a loop:

- the agent receives an input, which is a problem to solve or a task to perform
- the agent uses one or several tools to advance one step further. This tool can be anything: start a reasoning chain, search the web, call an API, write and execute some code..

These tools are often executed in a sandboxed environment, and most of them can be pre-written by us developers beforehand.

- the agent collects the tool outputs and starts a new loop, with newer information helping it better understand the solution.

To finish the loop, the agent will often have a tool to generate a final report and/or its own output, thus ending its work.
