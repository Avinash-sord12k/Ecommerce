from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config import Base
from app.subcategories.schema import product_subcategory_association


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
    is_active = Column(Boolean, default=True, nullable=False)

    # One-to-many relationship with Category
    category = relationship("Category", back_populates="products")

    # Many-to-many relationship with SubCategory
    sub_categories = relationship(
        "SubCategory",
        secondary=product_subcategory_association,
        back_populates="products",
    )
