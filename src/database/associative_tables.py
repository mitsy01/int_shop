from sqlalchemy import ForeignKey, Table, Column

from src.database.base import Base

prod_reviw_tabl_assoc = Table(
    "prod_reviw_tabl_assoc",
    Base.metadata,
    Column("prod_id", ForeignKey("products.id"), primary_key=True),
    Column("rev_id", ForeignKey("reviews.id"), primary_key=True)
)


user_prod_tabl_assoc = Table(
    "user_prod_tabl_assoc",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("prod_id", ForeignKey("products.id"), primary_key=True)
)


user_shoplist_tabl_assoc = Table(
    "user_shoplist_tabl_assoc",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("shop_list_id", ForeignKey("shop_list.id"), primary_key=True)
)


shop_list_prod_tabl_assoc = Table(
    "shop_list_prod_tabl_assoc",
    Base.metadata,
    Column("shop_list_id", ForeignKey("shop_list.id"), primary_key=True),
    Column("prod_id", ForeignKey("products.id"), primary_key=True)
)