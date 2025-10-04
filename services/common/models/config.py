import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Numeric,
    Interval, TIMESTAMP, func, UniqueConstraint, Float
)
import datetime as dt
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Setting(Base):
    __tablename__ = "settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String, nullable=False)
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False)
    value_type = Column(String, nullable=False, default="str")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    updated_by = Column(String)

    __table_args__ = (
        # Забороняємо дублікати ключів у межах сервісу
        {"sqlite_autoincrement": True},
    )
class Command(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True, index=True)
    command = Column(String, unique=True, nullable=False)
    group_name = Column(String, nullable=False)
    description = Column(Text)
class GroupIcon(Base):
    __tablename__ = "group_icons"
    group_name = Column(String, primary_key=True)
    icon = Column(String, nullable=False)
class Timeframe(Base):
    __tablename__ = "timeframes"

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    history_limit = Column(Integer, nullable=True)
    min_len = Column(Integer, nullable=True)
    hours = Column(Float, nullable=True)
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False
    )
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="timeframes")
class ReasonCode(Base):
    __tablename__ = "reason_codes"
    code = Column(String, primary_key=True)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # BUY / SELL / FILTER / MANUAL
class TradeProfile(Base):
    __tablename__ = "trade_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # нові поля
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False
    )

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="trade_profiles")
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="trade_profiles")
    conditions: Mapped[List["TradeCondition"]] = relationship(
        "TradeCondition", back_populates="profile", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<TradeProfile {self.id} user={self.user_id} exchange={self.exchange_id}>"
class TradeCondition(Base):
    __tablename__ = "trade_conditions"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("trade_profiles.id"))
    action = Column(String, nullable=False)  # BUY_BLOCKER, BUY_TRIGGER, SELL_TRIGGER
    condition_type = Column(String, nullable=False)
    param_1 = Column(Numeric)
    param_2 = Column(Numeric)
    priority = Column(Integer, nullable=False)

    profile = relationship("TradeProfile", back_populates="conditions")

    __table_args__ = (
        UniqueConstraint("profile_id", "action", "condition_type", "priority",
                         name="uq_trade_condition"),
    )

TradeProfile.conditions = relationship("TradeCondition", back_populates="profile")
