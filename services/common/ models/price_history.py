from sqlalchemy import Column, BigInteger, Text, Numeric, TIMESTAMP, text
from .base import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    exchange = Column(Text, nullable=False)
    symbol   = Column(Text, nullable=False)
    price    = Column(Numeric, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
