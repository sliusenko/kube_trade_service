# app/models/user.py
import uuid
import datetime as dt
from typing import Optional, List

from sqlalchemy import (
    Text, String, Boolean, TIMESTAMP,
    ForeignKey, func, text, Enum, Index, Integer, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


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

    trade_profiles: Mapped[List["TradeProfile"]] = relationship(
        "TradeProfile", back_populates="user", cascade="all, delete"
    )
    exchange_accounts: Mapped[List["UserExchangeAccount"]] = relationship(
        "UserExchangeAccount",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    __table_args__ = (
        Index("ix_users_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<User {self.user_id} {self.username}>"
class UserExchangeAccount(Base):
    __tablename__ = "user_exchange_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    exchange_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exchanges.id", ondelete="CASCADE"), nullable=False)

    alias: Mapped[str] = mapped_column(Text, nullable=False)
    account_type: Mapped[str] = mapped_column(Text, nullable=False, default="spot")

    # --- auth type: api_key / oauth
    auth_type: Mapped[str] = mapped_column(Enum("api_key", "oauth", name="exchange_auth_type"), nullable=False, default="api_key")

    # --- API credentials
    encrypted_api_key: Mapped[Optional[str]] = mapped_column(Text)
    encrypted_api_secret: Mapped[Optional[str]] = mapped_column(Text)

    # --- OAuth tokens
    oauth_provider: Mapped[Optional[str]] = mapped_column(Text)
    oauth_access_token: Mapped[Optional[str]] = mapped_column(Text)
    oauth_refresh_token: Mapped[Optional[str]] = mapped_column(Text)
    oauth_expires_at: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))
    scope: Mapped[Optional[str]] = mapped_column(Text)
    last_token_refresh: Mapped[Optional[dt.datetime]] = mapped_column(TIMESTAMP(timezone=True))
    token_status: Mapped[Optional[str]] = mapped_column(Text)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[dt.datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # --- relationships
    user: Mapped["User"] = relationship(back_populates="exchange_accounts")
    exchange: Mapped["Exchange"] = relationship(back_populates="user_accounts")
    trade_profiles: Mapped[List["TradeProfile"]] = relationship(
        "TradeProfile", back_populates="account", cascade="all, delete"
    )
    __table_args__ = (
        UniqueConstraint("user_id", "exchange_id", "alias", name="uq_user_exchange_alias"),
    )
class UserActiveSymbols(Base):
    __tablename__ = "user_active_symbols"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    trade_profile_id: Mapped[int] = mapped_column(
        ForeignKey("trade_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_exchange_account_id: Mapped[int] = mapped_column(
        ForeignKey("user_exchange_accounts.id", ondelete="CASCADE"),
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    auto_trade_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))

    created_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # --- Relationships
    user: Mapped["User"] = relationship()
    exchange: Mapped["Exchange"] = relationship()
    trade_profile: Mapped["TradeProfile"] = relationship(back_populates="active_symbols")
    account: Mapped["UserExchangeAccount"] = relationship()

    __table_args__ = (
        UniqueConstraint("user_id", "exchange_id", "symbol", "user_exchange_account_id",
                         name="uq_active_symbol_per_account"),
    )

    def __repr__(self) -> str:
        return f"<UserActiveSymbols {self.symbol} user={self.user_id} account={self.user_exchange_account_id}>"
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
class Permission(Base):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # relationships
    roles: Mapped[List["RolePermission"]] = relationship(  # type: ignore[name-defined]
        back_populates="permission",
    )

    def __repr__(self) -> str:
        return f"<Permission {self.name}>"
class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_name: Mapped[str] = mapped_column(
        Text, ForeignKey("roles.name", ondelete="CASCADE"), primary_key=True
    )
    permission_name: Mapped[str] = mapped_column(
        Text, ForeignKey("permissions.name", ondelete="CASCADE"), primary_key=True
    )

    # relationships
    role: Mapped["Role"] = relationship(  # type: ignore[name-defined]
        back_populates="permissions"
    )
    permission: Mapped["Permission"] = relationship(  # type: ignore[name-defined]
        back_populates="roles"
    )

    def __repr__(self) -> str:
        return f"<RolePermission role={self.role_name} permission={self.permission_name}>"
