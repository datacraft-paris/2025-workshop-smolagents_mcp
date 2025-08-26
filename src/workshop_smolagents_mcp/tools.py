import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from sqlalchemy import create_engine, text
from smolagents import tool


@tool
def query_events_db(query: str) -> str:
    """
    Allows querying the `evenements` table, which contains cleaned information about workshops and events.

    Table: evenements

    # TODO: add docstrings information relevant for the agent using the tool (e.g. available columns, examples queries, etc..)
    """
    # TODO: fill the tool
    pass

@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return the top 3 results with title and URL.
    Args:
        query: ...
    
    Returns:
        ...
    """
    # TODO: fill the tool
    pass

@tool
def summarize_url(url: str) -> str:
    """
    Summarize the content of a webpage using beautifulsoup.

    Args:
        url: A valid HTTP or HTTPS URL pointing to a public webpage.
    
    Returns:
        A raw text excerpt of the page content, suitable for summarization.
    """
    # TODO: fill the tool
    pass
