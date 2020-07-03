from decimal import Decimal

from sqlalchemy.orm import Session

from bank import crud
from bank.models import Wallet
from bank.schemas.wallet import WalletCreate


def test_create_wallet(db: Session) -> None:
    wallet_in = WalletCreate()
    wallet = crud.wallet.create(db=db, obj_in=wallet_in)
    assert wallet.balance == 0


def test_deposit_wallet(db: Session) -> None:
    wallet = Wallet(balance=2)
    db.add(wallet)
    wallet = crud.wallet.deposit(db=db, db_obj=wallet, amount=Decimal("1.1"))
    assert wallet.balance == Decimal("3.1")
    assert wallet.transactions[0].amount == Decimal("1.1")
