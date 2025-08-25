# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# # Web Search & Summarization Agent with Smolagent
#
# In this notebook, we will build a natural language agent capable of:
#
# - Searching the web based on user queries  
# - Automatically extracting and summarizing content from the resulting pages  
# - Returning structured answers, powered by a large language model (LLM)
#
# We will use the [`smolagents`](https://github.com/smol-ai/smolagent) framework to connect tools like `DuckDuckGo` search and HTML scraping with an OpenAI model.
#
#
# ## Example use case
#
# > "Summarize the Hugging Face blog post about open LLMs from 2023."
#
# The agent will:
# 1. Search the web for that blog post
# 2. Find the best link
# 3. Read and clean the content of the page
# 4. Summarize

# +
import os
from smolagents import CodeAgent, tool
from smolagents import OpenAIServerModel
from dotenv import load_dotenv
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

load_dotenv(override=True)


# -

# ### Tool: `web_search(query: str)`
#
# This tool enables the agent to **search the web using DuckDuckGo**.  
# It returns the **top 3 relevant results**, each with a title and a clickable URL.
#
# LLMs don’t have live access to the internet by default.  
#
# Example queries the agent might use this tool for:
# - `"latest news about open-source LLMs"`
# - `"hugging face blog post on quantization"`
# - `"datacraft website upcoming events"`
#
# #### How it works
#
# - The tool uses the [`ddgs`](https://pypi.org/project/ddgs/) library (DuckDuckGo Search).
# - It performs a web search for the given query.
# - It returns the first 3 results as a bullet list: `"- [title] ([url])"`

@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return the top 3 results with title and URL.

    Args:
        query: The search query to submit to the search engine.
    
    Returns:
        A short list of search results with titles and links.
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region="wt-wt", safesearch="Off", max_results=3):
            results.append(f"- {r['title']} ({r['href']})")
    return "\n".join(results)


# ### Tool: `summarize_url(url: str)`
#
# This tool allows the agent to **extract and summarize the main textual content** from a public web page.
#
# It plays a key role in helping the agent “read the web” by turning a full HTML page into a clean, readable excerpt — ready to be summarized by the LLM.
#
# After finding a link with `web_search(...)`, the agent needs to access and understand what’s on that page.  
#
# This tool:
# - Downloads the page (`requests`)
# - Parses it (`BeautifulSoup`)
# - Removes all unnecessary tags (e.g. `<script>`, `<style>`, `<noscript>`)
# - Extracts **only the visible text**
# - Returns the **first 60 lines** as a preview, making it manageable for summarization
#
#
#
# - **Input**: a valid URL (starting with `http://` or `https://`)
# - **Output**: a cleaned block of raw text, ready to be passed to the model
#
# If the page is unreachable, the tool returns a fallback error message.

@tool
def summarize_url(url: str) -> str:
    """
    Downloads and summarizes the readable text content of a given webpage.

    Args:
        url: A valid HTTP or HTTPS URL pointing to a public webpage.
    
    Returns:
        A raw text excerpt of the page content, suitable for summarization.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator="\n", strip=True)
        short_text = "\n".join(text.splitlines()[:60])  # limit to 60 lines

        return short_text if short_text else "No readable content found."
    except Exception as e:
        return f"Failed to summarize URL: {e}"


model = OpenAIServerModel(
    model_id="gpt-4o",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"]
)

# ### Creating an Agent with Multiple Tools
#
# Now that we’ve defined two tools — `web_search` and `summarize_url` — we can combine them into a single agent.
#
# By passing **both tools** to the `CodeAgent`, the model gains the ability to:
#
# 1. **Search the web** for relevant information (via `web_search`)
# 2. **Read and extract the content** of a webpage (via `summarize_url`)
#
#
# The `CodeAgent` uses the language model to reason about the user’s question and **decide when and how to call each tool**.  
# This means you don’t need to manually control the flow — the agent will:
#
# - Interpret the user's intent
# - Call one or both tools as needed
# - Return a natural language answer
#
#  For example, if you ask:
# > *"Summarize the latest blog post from Hugging Face about open LLMs"*  
#  
#  The agent might:
# 1. Use `web_search` to find the link
# 2. Use `summarize_url` on that link
# 3. Return a final summary

agent = CodeAgent(
    tools=[web_search, summarize_url],
    model=model,
)

question = "What is datacraft paris?"
agent.run(question)
