import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Numeric,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from bank.db.base_class import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    wallet = relationship("Wallet", back_populates="transactions")
    wallet_id = Column(Integer, ForeignKey("wallet.id"))
    amount = Column(Numeric, nullable=False, index=True)

    __table_args__ = (CheckConstraint(amount != 0),)
