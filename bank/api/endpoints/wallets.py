from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic.schema import date as date_type
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse

from bank import crud, schemas
from bank.api import deps
from bank.models import Transaction
from bank.schemas.transaction import TransactionDirection

router = APIRouter()


@router.get("/", response_model=List[schemas.Wallet])
def read_wallets(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve wallets.
    """
    return crud.wallet.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Wallet)
def create_wallet(
    *,
    db: Session = Depends(deps.get_db),
    # wallet_in: schemas.WalletCreate,
) -> Any:
    """
    Create new wallet.
    """
    return crud.wallet.create(db=db)


@router.get("/{id}", response_model=schemas.Wallet)
def read_wallet(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get item by ID.
    """
    if (wallet := crud.wallet.get(db=db, id=id)) is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.post("/{id}/deposit/", response_model=schemas.Wallet)
def deposit(
    *, db: Session = Depends(deps.get_db), id: int, deposit_in: schemas.WalletDeposit,
) -> Any:
    """
    Deposit wallet
    """
    wallet = crud.wallet.get_for_update(db=db, id=id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    crud.wallet.deposit(db=db, db_obj=wallet, amount=deposit_in.amount)
    db.commit()
    return wallet


@router.get("/{id}/transactions/", response_class=PlainTextResponse)
def transactions(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    date: Optional[date_type] = None,
    direction: Optional[TransactionDirection] = None,
) -> Any:
    """
    Show all transactions for the wallet
    """
    wallet = crud.wallet.get_for_update(db=db, id=id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    query = db.query(Transaction).filter(Transaction.wallet_id == id)
    if date:
        query = query.filter(func.DATE(Transaction.datetime) == date)
    if direction:
        if direction == TransactionDirection.deposit:
            query = query.filter(Transaction.amount > 0)
        elif direction == TransactionDirection.withdrawal:
            query = query.filter(Transaction.amount < 0)
        else:
            raise HTTPException(
                status_code=403, detail="Unsupported transaction direction"
            )

    fields = ["amount", "datetime"]
    rows = ""
    for transaction in query:
        rows += "\n" + ",".join(
            map(str, [getattr(transaction, field) for field in fields])
        )
    if not rows:
        raise HTTPException(status_code=404, detail="No transactions found")
    header = ",".join(fields)
    return header + rows
