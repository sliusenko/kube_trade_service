from sqlalchemy import Column, BigInteger, Text, Numeric, TIMESTAMP, text
from .base import Base

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
