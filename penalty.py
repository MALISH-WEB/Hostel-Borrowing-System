"""Penalty and dispute classes for the Hostel Borrowing System.

Member 5 implementation.
No third-party packages are required.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum


def _money(value, field_name):
    """Convert a number to Decimal and reject negative or invalid amounts."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.") from None

    if not amount.is_finite() or amount < 0:
        raise ValueError(f"{field_name} must be zero or greater.")
    return amount.quantize(Decimal("0.01"))


class Penalty(ABC):
    """Base class for all penalties.

    Every penalty subclass must implement calculate().
    """

    def __init__(self, description="Borrowing penalty"):
        self.description = description

    @abstractmethod
    def calculate(self) -> Decimal:
        """Return the penalty amount."""
        raise NotImplementedError


class LateFeePenalty(Penalty):
    """Penalty calculated as days late multiplied by the daily rate."""

    def __init__(self, days_late, daily_rate):
        super().__init__("Late return fee")
        if not isinstance(days_late, int) or isinstance(days_late, bool):
            raise ValueError("days_late must be a whole number.")
        if days_late < 0:
            raise ValueError("days_late cannot be negative.")
        self.days_late = days_late
        self.daily_rate = _money(daily_rate, "daily_rate")

    def calculate(self) -> Decimal:
        return (Decimal(self.days_late) * self.daily_rate).quantize(
            Decimal("0.01")
        )


class DamagePenalty(Penalty):
    """Penalty based on the cost of repairing a damaged item."""

    def __init__(self, repair_cost):
        super().__init__("Damage repair fee")
        self.repair_cost = _money(repair_cost, "repair_cost")

    def calculate(self) -> Decimal:
        return self.repair_cost


class LossPenalty(Penalty):
    """Penalty for a lost item: item value minus any deposit paid.

    The amount is not allowed to fall below zero.
    """

    def __init__(self, item_value, deposit=0):
        super().__init__("Lost item fee")
        self.item_value = _money(item_value, "item_value")
        self.deposit = _money(deposit, "deposit")

    def calculate(self) -> Decimal:
        amount = self.item_value - self.deposit
        return max(Decimal("0.00"), amount).quantize(Decimal("0.01"))


class DisputeStatus(Enum):
    """Possible stages of a penalty dispute."""

    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    SENT_TO_WARDEN = "Sent to warden"
    UNDER_REVIEW = "Under review"
    RESOLVED = "Resolved"


@dataclass
class Dispute:
    """A borrower's challenge to a penalty.

    Create a dispute, call submit(), then forward_to_warden().
    The warden can record a decision using resolve().
    """

    borrower: str
    penalty: Penalty
    reason: str
    status: DisputeStatus = DisputeStatus.DRAFT
    warden_response: str = ""

    def __post_init__(self):
        if not self.borrower or not self.borrower.strip():
            raise ValueError("Borrower name is required.")
        if not isinstance(self.penalty, Penalty):
            raise TypeError("penalty must be a Penalty object.")
        if not self.reason or not self.reason.strip():
            raise ValueError("A reason for the dispute is required.")

    def submit(self):
        """Record that the borrower has formally contested the penalty."""
        if self.status is not DisputeStatus.DRAFT:
            raise ValueError("Only a draft dispute can be submitted.")
        self.status = DisputeStatus.SUBMITTED

    def forward_to_warden(self):
        """Send a submitted dispute to the warden."""
        if self.status is not DisputeStatus.SUBMITTED:
            raise ValueError("Submit the dispute before sending it to the warden.")
        self.status = DisputeStatus.SENT_TO_WARDEN

    def mark_under_review(self):
        """Mark the dispute as being reviewed by the warden."""
        if self.status is not DisputeStatus.SENT_TO_WARDEN:
            raise ValueError("Only a dispute sent to the warden can be reviewed.")
        self.status = DisputeStatus.UNDER_REVIEW

    def resolve(self, warden_response):
        """Record the warden's decision and close the dispute."""
        if self.status not in (
            DisputeStatus.SENT_TO_WARDEN,
            DisputeStatus.UNDER_REVIEW,
        ):
            raise ValueError("The dispute must be with the warden before resolution.")
        if not warden_response or not warden_response.strip():
            raise ValueError("The warden's response cannot be empty.")
        self.warden_response = warden_response.strip()
        self.status = DisputeStatus.RESOLVED


if __name__ == "__main__":
    late = LateFeePenalty(days_late=3, daily_rate=2000)
    damage = DamagePenalty(repair_cost=15000)
    loss = LossPenalty(item_value=50000, deposit=10000)

    print(f"Late fee: UGX {late.calculate():,.2f}")
    print(f"Damage fee: UGX {damage.calculate():,.2f}")
    print(f"Loss fee: UGX {loss.calculate():,.2f}")

    dispute = Dispute(
        borrower="Amina",
        penalty=late,
        reason="I returned the item on the agreed date.",
    )
    dispute.submit()
    dispute.forward_to_warden()
    print(f"Dispute status: {dispute.status.value}")
