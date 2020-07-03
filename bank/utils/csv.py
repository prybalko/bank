from typing import List, Optional

from bank.db.base_class import Base


def to_csv(
    db_objects: List[Base], *, fields: List[str], include_header: Optional[bool] = True
) -> str:
    """
    Create a csv representation of db_objects
    """
    header = ",".join(fields) if include_header else ""
    rows = ""
    for transaction in db_objects:
        rows += "\n" + ",".join(
            map(str, [getattr(transaction, field) for field in fields])
        )
    return header + rows
