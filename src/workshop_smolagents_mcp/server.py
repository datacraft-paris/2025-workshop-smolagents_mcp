import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP
from workshop_smolagents_mcp.event import Event

# TODO: name your mcp server
mcp = FastMCP(...)

# TODO: name the mcp tool
@mcp.tool(name=..., description=...)
async def parse_datacraft_events() -> list[Event]:
    """Parse events from datacraft.paris agenda page"""
    # TODO: Fill the url variable with the correct url (datacraft.paris agenda page)
    url = "..."
    async with httpx.AsyncClient() as client:
        # TODO: use the client to make a get request to the url.
        response = await ...
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    events = []

    # Find events container
    # TODO: find the events container using the soup object
    # Hint: it has a class attribute equal to "tribe-events-calendar-list"
    events_container = ...
    event_containers = events_container.find_all(
        class_="tribe-events-calendar-list__event-wrapper"
    )

    for event_container in event_containers:
        event_title_component = event_container.find(
            class_="tribe-events-calendar-list__event-title-link"
        )
        event_title = event_title_component.text.strip().strip()
        event_url = event_title_component["href"].strip()
        event_datetime_component = event_container.find(
            class_="tribe-events-calendar-list__event-datetime"
        )
        event_date = event_datetime_component.find(class_="dateshed").text.strip()
        event_time = event_datetime_component.find(class_="timeshed").text.strip()
        event_location = event_container.find(
            class_="tribe-events-calendar-list__event-venue"
        ).text.strip()
        # TODO: append a new Event object to the events list
        events.append(
            ...
        )

    return events

# TODO: run the MCP server using by wrapping it in a if __name__ == "__main__" block
