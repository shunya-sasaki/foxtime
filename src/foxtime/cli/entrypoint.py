"""Entry point for the Foxtime CLI application."""

import random

from foxtime.cli.banner import Banner
from foxtime.cli.rich_table import ScheduleTable
from foxtime.reader import OutlookCalendarReader


def main() -> None:
    """Entry point for the Foxtime CLI application."""
    random_number = random.random()
    if random_number < 0.5:
        Banner.print_banner()
    else:
        Banner.print_simple_banner()

    print("")

    events = OutlookCalendarReader.fetch_today_events_from_default_calendar()
    table = ScheduleTable(events)
    table.print()
