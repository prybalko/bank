from decimal import Decimal

from sqlalchemy.orm import Session

from bank.models import Transaction, Wallet


def deposit_wallet(db: Session, *, wallet: Wallet, amount: Decimal) -> Wallet:
    wallet.balance += amount
    transaction = Transaction(wallet=wallet, amount=float(amount))
    db.add(transaction)
    db.commit()
    db.refresh(wallet)
    return wallet
