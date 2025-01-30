from sqlalchemy import ForeignKey, Table, Column

from src.database.base import Base

prod_reviw_tabl_assoc = Table(
    "prod_reviw_tabl_assoc",
    Base.metadata,
    Column("prod_id", ForeignKey("products.id"), primary_key=True),
    Column("rev_id", ForeignKey("reviews.id"), primary_key=True)
)