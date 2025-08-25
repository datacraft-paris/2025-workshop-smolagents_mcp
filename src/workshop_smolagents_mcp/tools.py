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

    Available columns include:
    - nomenclature: unique identifier or code for the event (e.g. "0706-MiniFormation-Capdigital")
    - titre: ...
    - description: ...
    - date: date of the event, stored as text (e.g. "2024-06-03")
    - horaire: time slot or duration of the event (e.g. "9h00 - 17h30")
    - tag: optional topic tags (e.g. "#DataGouv", "#IA")
    - langue: ...

    You can write SQL queries such as:
    - SELECT titre FROM evenements WHERE langue = 'français';
    - SELECT COUNT(*) FROM evenements WHERE tag LIKE '%IA%';
    - SELECT DISTINCT langue FROM evenements;
    - SELECT * FROM evenements ORDER BY date DESC;

    Note: the `date` column is stored as text. If you need to sort or filter by date,
    you can use SQL date functions (e.g. `STRFTIME`) or cast the column as needed.

    Args:
        query: A valid SQL query string to execute on the `evenements` table.

    Returns:
        A string containing the query results in plain text format.
    """
    engine = create_engine("sqlite:///../../data/events.db")
    output = ""
    with engine.connect() as con:
        # TODO: Execute the query using con.execute and the `text` function
        rows = con.execute(...)
        for row in rows:
            output += "\n" + str(row)
    return output

@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return the top 3 results with title and URL.

    Args:
        query: ...
    
    Returns:
        ...
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region="wt-wt", safesearch="Off", max_results=3):
            results.append(f"- {r['title']} ({r['href']})")
    # TODO: transform the list of results into a "\n"-separated string using str.join
    return ...

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

        # TODO: Remove scripts and styles using tag.decompose()
        for tag in soup(["script", "style", "noscript"]):
            ...

        # Extract visible text
        text = soup.get_text(separator="\n", strip=True)
        short_text = "\n".join(text.splitlines()[:60])  # limit to 60 lines

        return short_text if short_text else "No readable content found."
    except Exception as e:
        return f"Failed to summarize URL: {e}"
