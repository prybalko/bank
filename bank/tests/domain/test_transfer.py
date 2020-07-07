from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bank.domain.transfer import transfer_money
from bank.models import Wallet


def test_transfer_happy_path(db: Session) -> None:
    wallet1 = Wallet(balance=0.1)
    wallet2 = Wallet(balance=0.2)
    db.add_all([wallet1, wallet2])
    db.commit()

    transfer_money(
        db, source_wallet=wallet1, destination_wallet=wallet2, amount=Decimal("0.1")
    )

    db.refresh(wallet1)
    db.refresh(wallet2)

    assert wallet1.balance == 0
    assert wallet1.transactions[-1].amount == Decimal("-0.1")
    assert wallet2.balance == Decimal("0.3")
    assert wallet2.transactions[-1].amount == Decimal("0.1")


def test_not_enough_money(db: Session) -> None:
    wallet1 = Wallet(balance=0.1)
    wallet2 = Wallet(balance=0.2)
    db.add_all([wallet1, wallet2])
    db.commit()

    with pytest.raises(IntegrityError):
        transfer_money(
            db, source_wallet=wallet1, destination_wallet=wallet2, amount=Decimal("1.1")
        )

    Session.rollback(db)
    db.refresh(wallet1)
    db.refresh(wallet2)

    assert wallet1.balance == Decimal("0.1")
    assert len(wallet1.transactions) == 0
    assert wallet2.balance == Decimal("0.2")
    assert len(wallet2.transactions) == 0
