from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic.schema import date as date_type
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse

from bank import crud, schemas
from bank.api import deps
from bank.domain.wallet import deposit_wallet
from bank.models import Transaction
from bank.schemas.transaction import TransactionDirection
from bank.utils.csv import to_csv

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

    wallet = deposit_wallet(db=db, wallet=wallet, amount=deposit_in.amount)
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

    query = db.query(Transaction).filter(Transaction.wallet_id == id).order_by(Transaction.datetime.desc())
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

    if not query:
        raise HTTPException(status_code=404, detail="No transactions found")
    return to_csv(query, fields=["amount", "datetime"])
