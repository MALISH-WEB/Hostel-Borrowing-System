# Hostel Borrowing System

## Project overview
The Hostel Borrowing System is an object-oriented Python application for hostel students who lend items to one another. It records borrowing requests, agreements, returns and penalties when an item is returned late, damaged or lost.

The project is divided among five team members. Each member works on a separate Git branch and owns the files assigned to them.

## Team work division
| Member | Responsibility | Main files |
|---|---|---|
| 1 | Project foundations, enums and custom exceptions | `enums.py`, `exceptions.py`, `mixins.py` |
| 2 | Student and item information | `student.py`, `item.py` |
| 3 | Borrowing requests, messages and demonstration | `request.py`, `main.py` |
| 4 | Borrowing agreement and return process | `agreement.py` |
| 5 | Penalties, disputes and documentation | `penalty.py`, `README.md`, UML diagram |

## Member 5: Penalties and disputes
The penalty module contains a common abstract `Penalty` class and three penalty types.

### Penalty types
- **LateFeePenalty:** `days_late × daily_rate`.
- **DamagePenalty:** the repair cost of the damaged item.
- **LossPenalty:** `item_value − deposit`. The calculated amount is not allowed to be negative.

All money values are represented with Python's `Decimal` type to avoid common floating-point rounding problems. Amounts must be valid and non-negative.

### Dispute process
A borrower can challenge a penalty by creating a `Dispute` with their name, the penalty being challenged and a reason.

The dispute moves through these stages:

1. `DRAFT` – the dispute has been created.
2. `SUBMITTED` – the borrower has formally contested the penalty.
3. `SENT_TO_WARDEN` – the dispute has been forwarded to the warden.
4. `UNDER_REVIEW` – the warden is reviewing it.
5. `RESOLVED` – the warden's response has been recorded.

The class checks the order of these actions and raises `ValueError` if an invalid transition is attempted.

## Requirements
- Python 3.10 or later is recommended.
- No third-party packages are required for `penalty.py`.

## Running the penalty demonstration
From the project folder, run:

```bash
python penalty.py
```

Example output:

```text
Late fee: UGX 6,000.00
Damage fee: UGX 15,000.00
Loss fee: UGX 40,000.00
Dispute status: Sent to warden
```

## Example usage
```python
from penalty import LateFeePenalty, DamagePenalty, LossPenalty, Dispute

late_fee = LateFeePenalty(days_late=3, daily_rate=2000)
print(late_fee.calculate())  # 6000.00

damage_fee = DamagePenalty(repair_cost=15000)
print(damage_fee.calculate())  # 15000.00

loss_fee = LossPenalty(item_value=50000, deposit=10000)
print(loss_fee.calculate())  # 40000.00

dispute = Dispute(
    borrower="Amina",
    penalty=late_fee,
    reason="I returned the item on the agreed date.",
)
dispute.submit()
dispute.forward_to_warden()
dispute.mark_under_review()
dispute.resolve("The warden reviewed the evidence and cancelled the fee.")
```

## Integration notes for the team
- `penalty.py` is designed to be imported by the other project modules.
- Member 4's agreement/return logic can create the appropriate penalty object when an item is late, damaged or lost.
- Member 3 can demonstrate penalties and disputes in `main.py` after the other modules have been merged.
- The current brief does not specify a shared currency field or a required penalty constructor signature. This implementation uses numeric amounts and labels the demonstration output in UGX.
- If the team agrees on different method or attribute names, coordinate before changing the public interface.

## Git workflow for Member 5
Work on the assigned branch, not directly on `main`.

```bash
git checkout main
git pull origin main
git checkout -b feature/penalties
```

If the branch already exists locally:
```bash
git checkout feature/penalties
git pull origin main
```

After adding the files:
```bash
git add penalty.py README.md uml.puml
git commit -m "Add penalty and dispute system documentation"
git push -u origin feature/penalties
```

Then open a Pull Request on GitHub:
- **Base repository:** the original team repository.
- **Base branch:** `main`.
- **Compare/head branch:** your fork's `feature/penalties` branch.

Ask another team member to review the pull request. Do not merge it yourself unless your team has agreed that you should.
