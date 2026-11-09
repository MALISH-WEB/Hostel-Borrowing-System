from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
from datetime import date, timedelta
from penalty import LossPenalty, _money


class AgreementStatus(Enum):
    """Possible stages of a borrowing agreement."""

    PROPOSED = "Proposed"
    ACCEPTED = "Accepted"
    ACTIVE = "Active"
    RETURNED = "Returned"
    LOST = "Lost"


@dataclass
class ReturnRecord:
    """Stores details of a returned borrowed item."""

    item: str
    borrower: str
    return_date: date
    expected_return_date: date
    days_late: int

    def __post_init__(self):
        if self.days_late < 0:
            raise ValueError("Days late cannot be negative.")


@dataclass
class BorrowAgreement:
    """Manages the borrowing process from proposal to return."""

    item: str
    lender: str
    borrower: str
    pickup_date: date
    number_of_days: int
    deposit: Decimal = Decimal("0.00")

    status: AgreementStatus = AgreementStatus.PROPOSED

    return_record: ReturnRecord = None

    def __post_init__(self):
        if not self.item or not self.item.strip():
            raise ValueError("Item name is required.")

        if not self.lender or not self.lender.strip():
            raise ValueError("Lender name is required.")

        if not self.borrower or not self.borrower.strip():
            raise ValueError("Borrower name is required.")

        if not isinstance(self.pickup_date, date):
            raise ValueError("Pickup date must be a date.")

        if not isinstance(self.number_of_days, int) or isinstance(
            self.number_of_days, bool
        ):
            raise ValueError("Number of days must be a whole number.")

        if self.number_of_days <= 0:
            raise ValueError("Number of days must be greater than zero.")

        self.deposit = _money(self.deposit, "deposit")

    @property
    def expected_return_date(self):
        """Calculate the expected return date."""
        return self.pickup_date + timedelta(days=self.number_of_days)

    def counter_offer(self, new_number_of_days, new_deposit=None):
        """Change proposed borrowing terms."""

        if self.status is not AgreementStatus.PROPOSED:
            raise ValueError("Counter-offers are only allowed for proposed agreements.")

        if not isinstance(new_number_of_days, int) or isinstance(
            new_number_of_days, bool
        ):
            raise ValueError("Number of days must be a whole number.")

        if new_number_of_days <= 0:
            raise ValueError("Number of days must be greater than zero.")

        self.number_of_days = new_number_of_days

        if new_deposit is not None:
            self.deposit = _money(new_deposit, "deposit")

    def accept(self):
        """Accept a proposed borrowing agreement."""

        if self.status is not AgreementStatus.PROPOSED:
            raise ValueError("Only proposed agreements can be accepted.")

        self.status = AgreementStatus.ACCEPTED

    def activate(self):
        """Activate an accepted borrowing agreement."""

        if self.status is not AgreementStatus.ACCEPTED:
            raise ValueError("Only accepted agreements can become active.")

        self.status = AgreementStatus.ACTIVE

    def is_overdue(self, check_date=None):
        """Check whether the borrowed item is overdue."""

        if self.status is not AgreementStatus.ACTIVE:
            return False

        if check_date is None:
            check_date = date.today()

        if not isinstance(check_date, date):
            raise ValueError("Check date must be a date.")

        return check_date > self.expected_return_date

    def record_return(self, return_date=None):
        """Record the return of a borrowed item."""

        if self.status is not AgreementStatus.ACTIVE:
            raise ValueError("Only active agreements can be returned.")

        if return_date is None:
            return_date = date.today()

        if not isinstance(return_date, date):
            raise ValueError("Return date must be a date.")

        if return_date < self.pickup_date:
            raise ValueError("Return date cannot be before pickup date.")

        days_late = max(
            0, (return_date - self.expected_return_date).days
        )

        self.return_record = ReturnRecord(
            item=self.item,
            borrower=self.borrower,
            return_date=return_date,
            expected_return_date=self.expected_return_date,
            days_late=days_late,
        )

        self.status = AgreementStatus.RETURNED

        return self.return_record

    def declare_lost(self, item_value):
        """Declare an active borrowed item lost and calculate its penalty."""

        if self.status is not AgreementStatus.ACTIVE:
            raise ValueError("Only active agreements can be declared lost.")

        loss_penalty = LossPenalty(
            item_value=item_value,
            deposit=self.deposit,
        )

        self.status = AgreementStatus.LOST

        return loss_penalty

  #TESTING#
if __name__ == "__main__":
    print("\n--- BORROWING AGREEMENT ---")

    agreement = BorrowAgreement(
        item="Laptop",
        lender="John",
        borrower="Amina",
        pickup_date=date(2026, 11, 1),
        number_of_days=7,
        deposit=10000,
    )

    print("Initial status:", agreement.status.value)

    agreement.counter_offer(
        new_number_of_days=10,
        new_deposit=15000,
    )

    print("New borrowing period:", agreement.number_of_days)
    print("New deposit:", agreement.deposit)

    agreement.accept()
    print("Status:", agreement.status.value)

    agreement.activate()
    print("Status:", agreement.status.value)

    print("Expected return date:", agreement.expected_return_date)

    print("Is overdue:", agreement.is_overdue(date(2026, 11, 15)))

    record = agreement.record_return(date(2026, 11, 15))

    print("\n--- RETURN RECORD ---")
    print("Item:", record.item)
    print("Borrower:", record.borrower)
    print("Expected return:", record.expected_return_date)
    print("Actual return:", record.return_date)
    print("Days late:", record.days_late)
    print("Agreement status:", agreement.status.value)

#DECLARING ITEM#
    print("\n--- DECLARE ITEM LOST ---")

    lost_agreement = BorrowAgreement(
        item="Projector",
        lender="James",
        borrower="Peter",
        pickup_date=date(2026, 11, 1),
        number_of_days=5,
        deposit=10000
    )

    lost_agreement.accept()
    lost_agreement.activate()

    penalty = lost_agreement.declare_lost(
        item_value=50000
    )

    print("Item:", lost_agreement.item)
    print("Status:", lost_agreement.status.value)
    print("Loss penalty:", penalty.calculate())
