"""Outlook sensitivity model."""

from __future__ import annotations

from enum import IntEnum


class Sensitivity(IntEnum):
    """Outlook sensitivity."""

    NORMAL = 0
    PERSONAL = 1
    PRIVATE = 2
    CONFIDENTIAL = 3
    UNKNOWN = -1

    @classmethod
    def safe(cls, value: int) -> Sensitivity:
        """Get the Sensitivity enum member for the given value."""
        try:
            return cls(value)
        except (TypeError, ValueError):
            return cls.UNKNOWN
