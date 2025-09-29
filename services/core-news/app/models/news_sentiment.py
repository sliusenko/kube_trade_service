from sqlalchemy import Column, Integer, Text, Numeric, TIMESTAMP
from sqlalchemy.orm import declarative_base

class NewsSentiment(Base):
    __tablename__ = "news_sentiment"

    id = Column(Integer, primary_key=True, index=True)
    published_at = Column(TIMESTAMP(timezone=False), nullable=False)
    title = Column(Text, nullable=False)
    summary = Column(Text)
    sentiment = Column(Numeric)
    source = Column(Text)
    pair = Column(Text)
    url = Column(Text)

    price_before = Column(Numeric)
    price_after_1h = Column(Numeric)
    price_after_6h = Column(Numeric)
    price_after_24h = Column(Numeric)

    price_change_1h = Column(Numeric)
    price_change_6h = Column(Numeric)
    price_change_24h = Column(Numeric)
