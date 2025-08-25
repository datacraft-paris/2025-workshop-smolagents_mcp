from pydantic import BaseModel

# TODO: fill title and url typing
class Event(BaseModel):
    title: ...
    date: str
    time: str
    url: ...
    location: str
