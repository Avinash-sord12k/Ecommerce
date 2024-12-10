from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config import Base
from app.permissions.schema import role_permission_association


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    users = relationship("User", back_populates="role")

    permissions = relationship(
        "Permission",
        secondary=role_permission_association,
        back_populates="roles",
    )
