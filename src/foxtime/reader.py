"""A module to read calendar events from Outlook using win32com."""

from __future__ import annotations

from datetime import datetime
from datetime import time
from datetime import timedelta
from typing import List
from typing import Optional

import pythoncom
import win32com.client

from foxtime.models import BusyStatus
from foxtime.models import CalendarEvent
from foxtime.models import Sensitivity


class OutlookCalendarReader:
    """A class to read calendar events from Outlook."""

    @staticmethod
    def _to_local_iso(dt) -> str:
        """Convert a datetime object to a local ISO 8601 string."""
        local_tz = datetime.now().astimezone().tzinfo
        if getattr(dt, "tzinfo", None) is None:
            dt = dt.replace(tzinfo=local_tz)
        else:
            dt = dt.astimezone(local_tz)
        return dt.isoformat()

    @staticmethod
    def _split_categories(cat: Optional[str]) -> List[str]:
        if not cat:
            return []
        return [c.strip() for c in cat.split(",") if c.strip()]

    @staticmethod
    def get_today_time_range() -> tuple[datetime, datetime]:
        """Get the start and end datetime for today."""
        now = datetime.now().astimezone()
        today_start = datetime.combine(now.date(), time.min, tzinfo=now.tzinfo)
        tomorrow_start = today_start + timedelta(days=1)
        return today_start, tomorrow_start

    @staticmethod
    def build_outlook_restrict_filter(
        start_dt: datetime, end_dt: datetime
    ) -> str:
        """Build a restrict filter string for Outlook items."""
        start_str = start_dt.strftime("%m/%d/%Y %I:%M %p")
        end_str = end_dt.strftime("%m/%d/%Y %I:%M %p")
        return f"[Start] < '{end_str}' AND [END] > '{start_str}'"

    @classmethod
    def modify_localtime(cls, dt, delta_hour: int = 9):
        """Modify the given datetime by subtracting delta_hour hours."""
        modified_dt = dt - timedelta(hours=delta_hour)
        return modified_dt

    @classmethod
    def appointment_to_event(cls, item) -> CalendarEvent:
        """Safely convert Outlook AppointmentItem to CalendarEvent."""
        subject = getattr(item, "Subject", "") or ""
        location = getattr(item, "Location", None)
        start = getattr(item, "Start", None)
        start = cls.modify_localtime(start)
        end = getattr(item, "End", None)
        end = cls.modify_localtime(end)
        all_day = bool(getattr(item, "AllDayEvent", False))
        is_recurring = bool(getattr(item, "IsRecurring", False))
        busy = BusyStatus.safe(getattr(item, "BusyStatus", None))
        sensitivity = Sensitivity.safe(getattr(item, "Sensitivity", None))
        organizer = getattr(item, "Organizer", None)
        req = getattr(item, "RequiredAttendees", None)
        opt = getattr(item, "OptionalAttendees", None)
        categories = cls._split_categories(getattr(item, "Categories", None))
        start_iso = cls._to_local_iso(start)
        end_iso = cls._to_local_iso(end)

        return CalendarEvent(
            id=getattr(item, "EntryID", None),
            subject=subject,
            location=location,
            start=start_iso,
            end=end_iso,
            is_all_day=all_day,
            is_recurring=is_recurring,
            busy_status=busy,
            sensitivity=sensitivity,
            organizer=organizer,
            required_attendees=req,
            optional_attendees=opt,
            categories=categories,
        )

    @classmethod
    def fetch_today_events_from_default_calendar(cls) -> list[CalendarEvent]:
        """Fetch today's events from the default calendar."""
        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNameSpace("MAPI")
            calendar = namespace.GetDefaultFolder(9)
            items = calendar.Items
            items.Sort("Start")
            items.IncludeRecurrence = True

            start_dt, end_dt = cls.get_today_time_range()
            restriction = cls.build_outlook_restrict_filter(start_dt, end_dt)
            restricted = items.Restrict(restriction)
            events: List[CalendarEvent] = []
            for item in restricted:
                try:
                    evt = cls.appointment_to_event(item)
                    events.append(evt)
                except Exception:
                    continue
            events.sort(key=lambda e: (e.start or ""))
            return events
        finally:
            pythoncom.CoUninitialize()
