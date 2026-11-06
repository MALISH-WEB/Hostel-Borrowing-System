"""Student: a hostel resident who can lend and borrow items."""
from __future__ import annotations

from itertools import count

from .item import Item


class Student:
    # Class attribute: one counter shared by ALL students, gives each a unique id.
    _ids = count(1)

    def __init__(self, name: str, phone: str, room_number: str) -> None:
        # Instance attributes: belong to this one student.
        self.student_id = next(Student._ids)
        self.name = name
        self.phone = phone
        self.room_number = room_number
        self._trust_score = 100          # "private": change it via the property
        self._items: list[Item] = []     # "private": exposed only as a read-only copy

    # ---- encapsulation: trust score always stays between 0 and 100 ----
    @property
    def trust_score(self) -> int:
        return self._trust_score

    @trust_score.setter
    def trust_score(self, value: int) -> None:
        self._trust_score = max(0, min(100, value))

    @property
    def items(self) -> tuple[Item, ...]:
        """A copy, so outside code cannot modify the private list."""
        return tuple(self._items)

    # ---- actions ----
    def list_item(self, name: str, category: str, estimated_value: float) -> Item:
        """Add an item this student owns and is willing to lend."""
        item = Item(name, category, estimated_value, owner=self)
        self._items.append(item)
        return item

    def post_request(self, item_needed: str, needed_from):
        """Ask for an item. Needs ItemRequest from Member 3 (request.py)."""
        from .request import ItemRequest   # imported here to avoid a circular import
        return ItemRequest(self, item_needed, needed_from)

    # ---- alternative constructor ----
    @classmethod
    def from_dict(cls, data: dict) -> Student:
        return cls(data["name"], data["phone"], data["room_number"])

    # ---- dunder methods ----
    def __str__(self) -> str:
        return f"{self.name} (room {self.room_number})"

    def __repr__(self) -> str:
        return f"Student(id={self.student_id}, name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.student_id == other.student_id   # same id = same student

    def __hash__(self) -> int:
        return hash(self.student_id)                 # needed because __eq__ is defined

    def __lt__(self, other: Student) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.trust_score < other.trust_score  # sorted(students) ranks by trust