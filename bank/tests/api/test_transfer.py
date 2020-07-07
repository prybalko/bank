from decimal import Decimal
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from bank.models import Wallet


@patch("bank.api.endpoints.transfer.transfer_money")
def test_transfer(mock_transfer_money, client: TestClient, db: Session) -> None:
    wallet1 = Wallet(balance=0.1)
    wallet2 = Wallet(balance=0.2)
    db.add_all([wallet1, wallet2])
    db.commit()

    data = dict(source_wallet=wallet1.id, destination_wallet=wallet2.id, amount=0.1)

    response = client.post("transfer/", json=data)
    assert response.status_code == 200
    assert mock_transfer_money.call_args[1]["source_wallet"].id == wallet1.id
    assert mock_transfer_money.call_args[1]["destination_wallet"].id == wallet2.id
    assert mock_transfer_money.call_args[1]["amount"] == Decimal("0.1")


def test_not_enough_money(client: TestClient, db: Session) -> None:
    wallet1 = Wallet(balance=0.1)
    wallet2 = Wallet(balance=0.2)
    db.add_all([wallet1, wallet2])
    db.commit()

    data = dict(source_wallet=wallet1.id, destination_wallet=wallet2.id, amount=1.1)

    response = client.post("transfer/", json=data)
    assert response.status_code == 403


def test_no_wallet_found(client: TestClient, db: Session) -> None:
    data = dict(source_wallet=-1, destination_wallet=-2, amount=1.1)
    response = client.post("transfer/", json=data)
    assert response.status_code == 404
