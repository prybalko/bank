from pydantic import BaseModel, validator, root_validator
from pydantic.types import Decimal


class TransferBase(BaseModel):
    amount: Decimal

    @validator("amount")
    def amount_mist_be_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v

    @validator("amount")
    def amount_mist_have_correct_precision(cls, v):
        if v.as_tuple().exponent < -2:
            raise ValueError("amount must have 2 or less digits after decimal point")
        return v


class Transfer(TransferBase):
    source_wallet: int
    destination_wallet: int

    @root_validator()
    def wallets_must_not_be_the_same(cls, values):
        assert (
            values["source_wallet"] != values["destination_wallet"]
        ), "wallets must be different"
        return values
