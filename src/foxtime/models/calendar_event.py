"""Calendar event data model."""

from typing import List
from typing import Optional

from pydantic import BaseModel


class CalendarEvent(BaseModel):
    """Calendar event data model."""

    id: Optional[str]
    subject: str
    location: Optional[str]
    start: str
    end: str
    is_all_day: bool
    is_recurring: bool
    busy_status: Optional[str]
    sensitivity: Optional[str]
    organizer: Optional[str]
    required_attendees: Optional[str]
    optional_attendees: Optional[str]
    categories: List[str]
