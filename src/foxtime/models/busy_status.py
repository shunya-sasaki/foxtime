"""Outlook busy status model."""

from __future__ import annotations

from enum import IntEnum


class BusyStatus(IntEnum):
    """Outlook busy status."""

    FREE = 0
    TENTATIVE = 1
    BUSY = 2
    OUT_OF_OFFICE = 3
    WORKING_ELSE_WHERE = 4
    UNKNOWN = -1

    @classmethod
    def safe(cls, value: int) -> BusyStatus:
        """Get the BusyStatus enum member for the given value."""
        try:
            return cls(value)
        except (TypeError, ValueError):
            return cls.UNKNOWN
