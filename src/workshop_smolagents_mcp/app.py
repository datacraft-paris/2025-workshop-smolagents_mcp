from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from sqlalchemy import create_engine, text
from typing import List
from fastmcp import FastMCP

# TODO: write a simple FastAPI app that wraps previously-defined function through get or post requests for simplicity.
app = ...

# Your fastAPI routes here


# TODO: convert the fastapi app into a MCP server
mcp = ...

if __name__ == "__main__":
    # TODO: run the mcp server
