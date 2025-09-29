from sqlalchemy import Column, BigInteger, Text, Numeric, TIMESTAMP, text
from .base import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    exchange = Column(Text, nullable=False)
    symbol   = Column(Text, nullable=False)
    price    = Column(Numeric, nullable=False)
    timestamp = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )


class NewsSentiment(Base):
    __tablename__ = "news_sentiment"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    published_at = Column(TIMESTAMP(timezone=True), nullable=False)
    title   = Column(Text, nullable=False)
    summary = Column(Text)
    sentiment = Column(Numeric)
    source  = Column(Text)
    pair    = Column(Text)
    url     = Column(Text)
