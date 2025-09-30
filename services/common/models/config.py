from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, Interval
from sqlalchemy.orm import relationship
from common.models.base import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    hierarchy_level = Column(Integer, nullable=False)


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
    code = Column(String, primary_key=True)  # "1m", "15m", "1h"
    history_limit = Column(Integer)
    min_len = Column(Integer)
    hours = Column(Numeric)  # e.g. 1/60, 1, 4
    lookback = Column(Interval)


class ReasonCode(Base):
    __tablename__ = "reason_codes"
    code = Column(String, primary_key=True)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # BUY / SELL / FILTER / MANUAL


class TradeProfile(Base):
    __tablename__ = "trade_profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)


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


TradeProfile.conditions = relationship("TradeCondition", back_populates="profile")
