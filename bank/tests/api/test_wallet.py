from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import exists
from sqlalchemy.orm import Session

from bank import crud
from bank.models import Wallet


def test_create_wallet(client: TestClient, db: Session) -> None:
    response = client.post(f"wallets/")
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["balance"] == 0
    assert db.query(exists().where(Wallet.id == content["id"])).scalar()


def test_read_wallet(client: TestClient, db: Session) -> None:
    wallet = Wallet(balance=72)
    db.add(wallet)
    db.commit()
    response = client.get(f"wallets/{wallet.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == wallet.id
    assert content["balance"] == wallet.balance


def test_deposit(client: TestClient, db: Session) -> None:
    wallet = Wallet(balance=Decimal("0.1"))
    db.add(wallet)
    db.commit()

    response = client.post(f"wallets/{wallet.id}/deposit/", json={"amount": 0.2})
    db.refresh(wallet)
    assert response.status_code == 200
    content = response.json()
    assert content["balance"] == float(wallet.balance)
    assert wallet.balance == Decimal("0.3")


def test_transactions(client: TestClient, db: Session) -> None:
    wallet = crud.wallet.create(db)
    crud.wallet.deposit(db=db, db_obj=wallet, amount=Decimal("1.1"))
    db.commit()

    response = client.get(f"wallets/{wallet.id}/transactions/")
    assert response.status_code == 200
    assert response.text == f"amount,datetime\n1.1,{wallet.transactions[0].datetime}"
