from sqlalchemy.orm import Session

from bank.models import Wallet
from bank.utils.csv import to_csv


def test_csv_with_header(db: Session) -> None:
    obj_1 = Wallet(id=1, balance=11)
    obj_2 = Wallet(id=2, balance=22)
    csv = to_csv([obj_1, obj_2], fields=["id", "balance"])
    assert csv == "id,balance\n1,11\n2,22"
