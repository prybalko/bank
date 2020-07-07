from sqlalchemy.orm import Session

from bank import crud
from bank.schemas.wallet import WalletCreate


def test_create_wallet(db: Session) -> None:
    wallet_in = WalletCreate()
    wallet = crud.wallet.create(db=db, obj_in=wallet_in)
    assert wallet.balance == 0
