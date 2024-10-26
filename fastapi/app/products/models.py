from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False, index=True)
    slug = Column(String(60), unique=True, nullable=False, index=True)
    tags = Column(String(255), nullable=True)
    discount = Column(Float, default=0.0)
    stock = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="products")
    sub_category_id = Column(
        Integer, ForeignKey("sub_categories.id"), nullable=True
    )
    sub_category = relationship("SubCategory", back_populates="products")
    is_active = Column(Boolean, default=True, nullable=False)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    products = relationship("Product", back_populates="category")


class SubCategory(Base):
    __tablename__ = "sub_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    products = relationship("Product", back_populates="sub_category")
