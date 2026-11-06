"""Item: something a student owns and can lend out."""
from __future__ import annotations

from itertools import count
from typing import TYPE_CHECKING

from .exceptions import ItemUnavailableError

if TYPE_CHECKING:  # only for type hints, avoids a circular import with student.py
    from .student import Student


class Item:
    # Class attribute: one counter shared by ALL items, gives each a unique id.
    _ids = count(1)

    def __init__(self, name: str, category: str, estimated_value: float,
                 owner: Student) -> None:
        self.item_id = next(Item._ids)
        self.name = name
        self.category = category
        self.estimated_value = estimated_value   # used by LossPenalty
        self.owner = owner                       # association: Item knows its Student
        self._available = True

    # ---- availability ----
    @property
    def is_available(self) -> bool:
        return self._available

    def mark_unavailable(self) -> None:
        """Called when the item is lent out."""
        if not self._available:
            raise ItemUnavailableError(f"'{self.name}' is already lent out")
        self._available = False

    def mark_available(self) -> None:
        """Called when the item comes back."""
        self._available = True

    # ---- dunder methods ----
    def __str__(self) -> str:
        return f"{self.name} [{self.category}]"

    def __repr__(self) -> str:
        return f"Item(id={self.item_id}, name={self.name!r})"