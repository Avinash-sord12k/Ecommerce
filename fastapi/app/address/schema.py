from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config import Base


class Address(Base):
    __tablename__ = "addresses"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name: str = Column(String(255), nullable=False)  # ex: home, office
    address: str = Column(String(255), nullable=False)
    city: str = Column(String(255), nullable=False)
    state: str = Column(String(255), nullable=False)
    zip_code: str = Column(String(255), nullable=False)
    country: str = Column(String(255), nullable=False)

    user = relationship("User", back_populates="addresses")
