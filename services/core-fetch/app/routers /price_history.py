from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from common.models.price_history import PriceHistory
from common.schemas.price_history import PriceHistoryInDB, PriceHistoryCreate
from common.deps.db import get_session

router = APIRouter(prefix="/price-history", tags=["price-history"])

@router.get("/", response_model=list[PriceHistoryInDB])
async def get_prices(limit: int = 50, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(PriceHistory).order_by(PriceHistory.timestamp.desc()).limit(limit)
    )
    return result.scalars().all()

@router.get("/{price_id}", response_model=PriceHistoryInDB)
async def get_price(price_id: int, session: AsyncSession = Depends(get_session)):
    db_price = await session.get(PriceHistory, price_id)
    if not db_price:
        raise HTTPException(status_code=404, detail="Price not found")
    return db_price

@router.post("/", response_model=PriceHistoryInDB)
async def create_price(price: PriceHistoryCreate, session: AsyncSession = Depends(get_session)):
    db_price = PriceHistory(**price.dict())
    session.add(db_price)
    await session.commit()
    await session.refresh(db_price)
    return db_price
