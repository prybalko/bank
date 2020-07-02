from enum import Enum

from pydantic import BaseModel
from pydantic.schema import datetime
from pydantic.types import Decimal


class Transaction(BaseModel):
    amount: Decimal
    datetime: datetime

    class Config:
        orm_mode = True


class TransactionDirection(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
