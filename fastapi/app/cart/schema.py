from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config import Base


class CartStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ABANDONED = "abandoned"


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50), nullable=False)
    reminder_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        Enum(CartStatus), default=CartStatus.ACTIVE, nullable=False
    )

    # One to many relationship with User
    user = relationship("User", back_populates="carts")

    # One to many relationship with CartItems
    cart_items = relationship(
        "CartItems", back_populates="cart", cascade="all, delete-orphan"
    )


class CartItems(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)

    # Relationships
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
