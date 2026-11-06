"""Custom exceptions for the hostel borrowing system.

Every error raised by this system inherits from HostelError, so callers can
catch the whole family with a single `except HostelError`.
"""


class HostelError(Exception):
    """Base class for all errors in this system."""


class ItemUnavailableError(HostelError):
    """The item is already lent out or otherwise not available."""


class InvalidTermsError(HostelError):
    """The agreement terms break a rule (e.g. duration over the limit)."""


class InvalidTransitionError(HostelError):
    """An agreement method was called in the wrong status."""