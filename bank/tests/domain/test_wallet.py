from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bank.domain.wallet import deposit_wallet
from bank.models import Wallet


def test_wallet_deposit(db: Session) -> None:
    wallet = Wallet(balance=0.1)
    db.add(wallet)
    db.commit()

    wallet = deposit_wallet(db, wallet=wallet, amount=Decimal("0.2"))

    assert wallet.balance == Decimal("0.3")
    assert wallet.transactions[0].amount == Decimal("0.2")


def test_negative_deposit(db: Session) -> None:
    wallet = Wallet(balance=0.1)
    db.add(wallet)
    db.commit()
    wallet_id = wallet.id

    with pytest.raises(IntegrityError):
        deposit_wallet(db, wallet=wallet, amount=Decimal("-0.2"))

    Session.rollback(db)
    wallet = db.query(Wallet).get(wallet_id)
    assert wallet.balance == Decimal("0.1")
    assert len(wallet.transactions) == 0


def test_zero_deposit(db: Session) -> None:
    wallet = Wallet(balance=0.1)
    db.add(wallet)
    db.commit()

    with pytest.raises(IntegrityError):
        deposit_wallet(db, wallet=wallet, amount=Decimal("0"))

    Session.rollback(db)
