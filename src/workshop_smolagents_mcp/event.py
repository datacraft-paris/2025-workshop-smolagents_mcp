from pydantic import BaseModel

class Event(BaseModel):
    title: str
    date: str
    time: str
    url: str
    location: str
