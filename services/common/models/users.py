# app/models/user.py
import uuid
import datetime as dt
from typing import Optional, List

from sqlalchemy import Text, String, Boolean, TIMESTAMP, ForeignKey, func, text, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.db.base import Base  # ваш Declarative Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # nullable=True за аналогією з вашим прикладом
    role: Mapped[Optional[str]] = mapped_column(
        Text, ForeignKey("roles.name", ondelete="CASCADE")
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )

    # relationships
    role_obj: Mapped[Optional["Role"]] = relationship(  # type: ignore[name-defined]
        back_populates="users"
    )

    __table_args__ = (
        Index("ix_users_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<User {self.user_id} {self.username}>"
class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # relationships
    users: Mapped[List["User"]] = relationship(  # type: ignore[name-defined]
        back_populates="role_obj",
        cascade="all, delete",
    )
    permissions: Mapped[List["RolePermission"]] = relationship(  # type: ignore[name-defined]
        back_populates="role",
    )

    def __repr__(self) -> str:
        return f"<Role {self.name}>"

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_name = Column(Text, ForeignKey("roles.name", ondelete="CASCADE"), primary_key=True)
    permission_name = Column(Text, ForeignKey("permissions.name", ondelete="CASCADE"), primary_key=True)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
class Permission(Base):
    __tablename__ = "permissions"

    name = Column(Text, primary_key=True)
    description = Column(Text)

    roles = relationship("RolePermission", back_populates="permission")
