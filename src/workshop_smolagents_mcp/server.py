import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP
from workshop_smolagents_mcp.event import Event


mcp = FastMCP("datacraft-events-mcp")


@mcp.tool(name="parse_datacraft_events", description="Parse events from datacraft.paris agenda page")
async def parse_datacraft_events() -> list[Event]:
    """Parse events from datacraft.paris agenda page"""
    url = "https://datacraft.paris/agenda/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    events = []

    # Find events container
    events_container = soup.find(class_="tribe-events-calendar-list")
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

        events.append(
            Event(
                title=event_title,
                url=event_url,
                date=event_date,
                time=event_time,
                location=event_location,
            )
        )

    return events

if __name__ == "__main__":
    mcp.run()
