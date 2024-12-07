from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # One-to-many relationship with SubCategory
    sub_categories = relationship("SubCategory", back_populates="category", cascade="all, delete-orphan")
