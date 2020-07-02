from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from bank.models import Wallet


def test_transfer(client: TestClient, db: Session) -> None:
    wallet1 = Wallet(balance=0.1)
    wallet2 = Wallet(balance=0.2)
    db.add_all([wallet1, wallet2])
    db.commit()

    data = dict(source_wallet=wallet1.id, destination_wallet=wallet2.id, amount=0.1)

    response = client.post("transfer/", json=data)
    assert response.status_code == 200

    db.refresh(wallet1)
    db.refresh(wallet2)

    assert wallet1.balance == 0
    assert wallet2.balance == Decimal("0.3")
