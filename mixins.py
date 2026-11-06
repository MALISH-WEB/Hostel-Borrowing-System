"""Small reusable classes that add one capability to others."""
from datetime import datetime


class TimestampMixin:
    """Gives any class a `created_at` timestamp.

    Uses *args/**kwargs and super().__init__ so it cooperates with other
    parent classes in the MRO (method resolution order).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()