"""Small verification script for Member 5's penalty module."""
from decimal import Decimal
from penalty import (
    LateFeePenalty, DamagePenalty, LossPenalty,
    Dispute, DisputeStatus
)

assert LateFeePenalty(3, 2000).calculate() == Decimal("6000.00")
assert DamagePenalty(15000).calculate() == Decimal("15000.00")
assert LossPenalty(50000, 10000).calculate() == Decimal("40000.00")
assert LossPenalty(5000, 7000).calculate() == Decimal("0.00")

penalty = LateFeePenalty(2, 1000)
dispute = Dispute("Amina", penalty, "The item was returned on time.")
dispute.submit()
assert dispute.status is DisputeStatus.SUBMITTED
dispute.forward_to_warden()
assert dispute.status is DisputeStatus.SENT_TO_WARDEN
dispute.mark_under_review()
dispute.resolve("Penalty cancelled after review.")
assert dispute.status is DisputeStatus.RESOLVED

print("All Member 5 checks passed.")
