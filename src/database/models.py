from typing import List
from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.associative_tables import prod_reviw_tabl_assoc

@dataclass
class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[str] = mapped_column(String(), primary_key=True)
    text: Mapped[str] = mapped_column(String())
    grade: Mapped[str] = mapped_column(String())
    
 
@dataclass   
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    img_url: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column()
    reviews: Mapped[List[Review]] = relationship(secondary=prod_reviw_tabl_assoc)