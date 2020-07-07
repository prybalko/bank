from decimal import Decimal

from sqlalchemy.orm import Session

from bank.models import Transaction, Wallet


def transfer_money(
    db: Session, *, source_wallet: Wallet, destination_wallet: Wallet, amount: Decimal
) -> None:
    source_wallet.balance -= amount
    db.add(Transaction(wallet=source_wallet, amount=-float(amount)))

    destination_wallet.balance += amount
    db.add(Transaction(wallet=destination_wallet, amount=float(amount)))

    db.commit()
