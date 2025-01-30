from typing import List

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy(model_class=Base, engine_options=dict(echo=True))

produ_reviw_tabl_assoc = Table(
    "produ_tabl_assoc",
    Base.metadata,
    Column("produ_id", ForeignKey("products.id"), primary_key=True),
    Column("reviw_id", ForeignKey("reviews.id"), primary_key=True)
)

class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[str] = mapped_column(String(), primary_key=True)
    text: Mapped[str] = mapped_column(String())
    grade: Mapped[str] = mapped_column(String())
    
    
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    img_url: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column()
    reviews: Mapped[List[Review]] = relationship(secondary=produ_reviw_tabl_assoc)