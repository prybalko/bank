from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bank import crud, schemas
from bank.api import deps
from bank.domain.transfer import transfer_money

router = APIRouter()


@router.post("/")
def transfer(
    *, db: Session = Depends(deps.get_db), transfer_in: schemas.Transfer,
) -> Any:
    """
    Transfer money from one wallet to another.
    """
    source_wallet = crud.wallet.get_for_update(db, transfer_in.source_wallet)
    if not source_wallet:
        raise HTTPException(status_code=404, detail="Source wallet not found")
    destination_wallet = crud.wallet.get_for_update(db, transfer_in.destination_wallet)
    if not destination_wallet:
        raise HTTPException(status_code=404, detail="Destination wallet not found")
    if source_wallet.balance < transfer_in.amount:
        raise HTTPException(status_code=403, detail="Insufficient funds")

    transfer_money(db, source_wallet=source_wallet, destination_wallet=destination_wallet, amount=transfer_in.amount)

    return {"status": "ok"}
