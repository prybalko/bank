from pydantic import BaseModel

from pydantic.types import Decimal

from bank.schemas.transfer import TransferBase


# Shared attributes
class WalletBase(BaseModel):
    pass


# Properties to receive via API on creation
class WalletCreate(WalletBase):
    pass


# # Properties to receive via API on update
class WalletUpdate(WalletBase):
    pass


# # Properties to receive via API on deposit
class WalletDeposit(TransferBase):
    amount: Decimal


class WalletInDBBase(WalletBase):
    id: int
    balance: Decimal

    class Config:
        orm_mode = True


# Additional properties to return via API
class Wallet(WalletInDBBase):
    pass
