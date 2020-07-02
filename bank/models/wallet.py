from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, CheckConstraint
from sqlalchemy.orm import relationship

from bank.db.base_class import Base


class Wallet(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Numeric, nullable=False, default=0,)
    transactions = relationship("Transaction", back_populates="wallet")

    __table_args__ = (CheckConstraint(balance >= 0),)
