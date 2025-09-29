from sqlalchemy import Column, BigInteger, Text, Numeric, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    exchange = Column(Text, nullable=False)
    pair = Column(Text, nullable=False)
    price = Column(Numeric, nullable=False)
