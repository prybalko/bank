# Import all the models, so that Base has them before being
# imported by Alembic
from bank.db.base_class import Base  # noqa
from bank.models.wallet import Wallet  # noqa
from bank.models.transaction import Transaction  # noqa
