"""Rich schedule table class."""

import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic import Field
from rich.console import Console
from rich.table import Table

from foxtime.models import CalendarEvent


class _TableRow(BaseModel):
    subject: str
    location: str
    start: str = Field()
    end: str = Field()
    timezone: str = "Asia/Tokyo"

    start_datetime: str = Field(default="00:00", init=False)
    end_datetime: str = Field(default="00:00", init=False)

    def model_post_init(self, context: Any, /) -> None:
        self.start_datetime = (
            datetime.datetime.fromisoformat(self.start)
            .astimezone(ZoneInfo(self.timezone))
            .strftime("%H:%M")
        )
        self.end_datetime = (
            datetime.datetime.fromisoformat(self.end)
            .astimezone(ZoneInfo(self.timezone))
            .strftime("%H:%M")
        )
        return super().model_post_init(context)


class ScheduleTable:
    """Rich format schedule table."""

    def __init__(
        self, events: list[CalendarEvent], title: str = "Schedule"
    ) -> None:
        """Initialize ScheduleTable instance."""
        self.events = events
        self.title = title

    def print(self):
        """Print rich formatted table."""
        table = Table(title=self.title)
        table.add_column("Subject")
        table.add_column("Location")
        table.add_column("Start")
        table.add_column("End")

        for event in self.events:
            if event.is_all_day:
                continue
            row = _TableRow.model_validate(event.model_dump(), extra="ignore")
            table.add_row(
                row.subject, row.location, row.start_datetime, row.end_datetime
            )
        console = Console()
        console.print(table)
