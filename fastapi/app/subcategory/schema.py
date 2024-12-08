from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.config import Base

product_subcategory_association = Table(
    "product_subcategory_association",
    Base.metadata,
    Column(
        "product_id",
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "sub_category_id",
        Integer,
        ForeignKey("sub_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class SubCategory(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationship back to Category
    category = relationship(
        "Category",
        back_populates="sub_categories",
    )

    # Many-to-many relationship with Product
    products = relationship(
        "Product",
        secondary=product_subcategory_association,
        back_populates="sub_categories",
    )
