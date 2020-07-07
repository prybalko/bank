from sqlalchemy.orm import Session

from bank.crud.base import CRUDBase
from bank.models.wallet import Wallet
from bank.schemas.wallet import WalletCreate, WalletUpdate


class CRUDWallet(CRUDBase[Wallet, WalletCreate, WalletUpdate]):
    def create(self, db: Session, *, obj_in: WalletCreate = None) -> Wallet:
        db_obj = Wallet()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


wallet = CRUDWallet(Wallet)
