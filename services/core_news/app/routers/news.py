from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from common.models.markethistory import NewsSentiment
from common.schemas.markethistory import NewsSentimentCreate, NewsSentimentOut, NewsSentimentUpdate
from common.deps.db import get_session

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=list[NewsSentimentOut])
async def get_all_news(limit: int = 50, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(NewsSentiment).order_by(NewsSentiment.published_at.desc()).limit(limit)
    )
    return result.scalars().all()

@router.get("/{news_id}", response_model=NewsSentimentOut)
async def get_news(news_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.get(NewsSentiment, news_id)
    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result

@router.post("/", response_model=NewsSentimentOut)
async def create_news(news: NewsSentimentCreate, session: AsyncSession = Depends(get_session)):
    db_news = NewsSentiment(**news.dict())
    session.add(db_news)
    await session.commit()
    await session.refresh(db_news)
    return db_news

@router.patch("/{news_id}", response_model=NewsSentimentOut)
async def update_news(news_id: int, news_update: NewsSentimentUpdate, session: AsyncSession = Depends(get_session)):
    db_news = await session.get(NewsSentiment, news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")

    for field, value in news_update.dict(exclude_unset=True).items():
        setattr(db_news, field, value)

    await session.commit()
    await session.refresh(db_news)
    return db_news

@router.delete("/{news_id}")
async def delete_news(news_id: int, session: AsyncSession = Depends(get_session)):
    db_news = await session.get(NewsSentiment, news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    await session.delete(db_news)
    await session.commit()
    return {"ok": True}
