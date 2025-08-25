from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from sqlalchemy import create_engine, text
from typing import List
from fastmcp import FastMCP

app = FastAPI(
    title="Workshop SmolAgents MCP API",
    description="API for querying events database, web search, and URL summarization",
    version="1.0.0"
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str

class WebSearchRequest(BaseModel):
    query: str

class SummarizeUrlRequest(BaseModel):
    url: str

class SearchResult(BaseModel):
    title: str
    url: str

class WebSearchResponse(BaseModel):
    results: List[SearchResult]

@app.get("/")
async def root():
    return {"message": "Workshop SmolAgents MCP API", "version": "1.0.0"}

# TODO: name the endpoint
@app.post("/...", response_model=str)
async def query_events_db(request: QueryRequest):
    """
    Query the events database with SQL.
    
    Available columns in the `evenements` table:
    - nomenclature: unique identifier
    - titre: title of the event
    - description: detailed description
    - date: date of the event (text format)
    - horaire: time slot
    - tag: topic tags
    - langue: language of the event
    """
    engine = create_engine("sqlite:///../../data/events.db")
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(request.query))
        for row in rows:
            output += "\n" + str(row)
    return output

# TODO: name the endpoint
@app.post("/...", response_model=WebSearchResponse)
async def web_search(request: WebSearchRequest):
    """
    Search the web using DuckDuckGo and return the top 3 results.
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(request.query, region="wt-wt", safesearch="Off", max_results=3):
            results.append(SearchResult(title=r['title'], url=r['href']))
    return WebSearchResponse(results=results)

# TODO: name the endpoint
@app.post("/...", response_model=str)
async def summarize_url(request: SummarizeUrlRequest):
    """
    Download and summarize the readable text content of a webpage.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(request.url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text
    text = soup.get_text(separator="\n", strip=True)
    short_text = "\n".join(text.splitlines()[:60])  # limit to 60 lines

    return short_text if short_text else "No readable content found."

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# TODO: convert the FastAPI app to a FastMCP app using FastMCP.from_fastapi
mcp = ...

if __name__ == "__main__":
    # TODO: run the mcp server using the `run` method of the mcp object
