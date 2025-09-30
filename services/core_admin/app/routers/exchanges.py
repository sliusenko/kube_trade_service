from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from common.deps.db import get_session
from common.models.exchanges import (
    Exchange, ExchangeCredential, ExchangeSymbol,
    ExchangeLimit, ExchangeStatusHistory, ExchangeFee
)
from common.schemas.exchanges import (
    ExchangeCreate, ExchangeUpdate, ExchangeRead,
    ExchangeCredentialCreate, ExchangeCredentialRead,
    ExchangeSymbolRead, ExchangeLimitRead,
    ExchangeStatusHistoryRead, ExchangeFeeRead
)

router = APIRouter(prefix="/exchanges", tags=["Exchanges"])

# ----------------------------------------------------------------
# Exchange CRUD
# ----------------------------------------------------------------
@router.get("/", response_model=List[ExchangeRead])
async def list_exchanges(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Exchange))
    return result.scalars().all()


@router.get("/{exchange_id}", response_model=ExchangeRead)
async def get_exchange(exchange_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Exchange).where(Exchange.id == exchange_id))
    exchange = result.scalar_one_or_none()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return exchange


@router.post("/", response_model=ExchangeRead)
async def create_exchange(payload: ExchangeCreate, db: AsyncSession = Depends(get_session)):
    exchange = Exchange(**payload.dict())
    db.add(exchange)
    await db.commit()
    await db.refresh(exchange)
    return exchange


@router.put("/{exchange_id}", response_model=ExchangeRead)
async def update_exchange(exchange_id: UUID, payload: ExchangeUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Exchange).where(Exchange.id == exchange_id))
    exchange = result.scalar_one_or_none()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(exchange, k, v)

    await db.commit()
    await db.refresh(exchange)
    return exchange


@router.delete("/{exchange_id}")
async def delete_exchange(exchange_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Exchange).where(Exchange.id == exchange_id))
    exchange = result.scalar_one_or_none()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")

    await db.delete(exchange)
    await db.commit()
    return {"status": "deleted"}

# ----------------------------------------------------------------
# Exchange Credentials
# ----------------------------------------------------------------
@router.get("/{exchange_id}/credentials", response_model=List[ExchangeCredentialRead],)
async def list_credentials(exchange_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(ExchangeCredential).where(ExchangeCredential.exchange_id == exchange_id)
    )
    return result.scalars().all()

@router.post("/{exchange_id}/credentials", response_model=ExchangeCredentialRead,)
async def add_credential(exchange_id: UUID, cred: ExchangeCredentialCreate, session: AsyncSession = Depends(get_session),):
    new_cred = ExchangeCredential(exchange_id=exchange_id, **cred.dict())
    session.add(new_cred)
    await session.commit()
    await session.refresh(new_cred)
    return new_cred

@router.put("/{exchange_id}/credentials/{cred_id}", response_model=ExchangeCredentialRead,)
async def update_credential(
    exchange_id: UUID,
    cred_id: UUID,
    cred: ExchangeCredentialUpdate,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(ExchangeCredential).where(
            ExchangeCredential.exchange_id == exchange_id,
            ExchangeCredential.id == cred_id,
        )
    )
    db_cred = result.scalar_one_or_none()
    if not db_cred:
        raise HTTPException(status_code=404, detail="Credential not found")

    for k, v in cred.dict(exclude_unset=True).items():
        setattr(db_cred, k, v)

    await session.commit()
    await session.refresh(db_cred)
    return db_cred

@router.delete("/{exchange_id}/credentials/{cred_id}", response_model=dict,)
async def delete_credential(exchange_id: UUID, cred_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(ExchangeCredential).where(
            ExchangeCredential.exchange_id == exchange_id,
            ExchangeCredential.id == cred_id,
        )
    )
    db_cred = result.scalar_one_or_none()
    if not db_cred:
        raise HTTPException(status_code=404, detail="Credential not found")

    await session.delete(db_cred)
    await session.commit()
    return {"ok": True}

# ----------------------------------------------------------------
# Exchange Symbols (read-only)
# ----------------------------------------------------------------
@router.get("/{exchange_id}/symbols", response_model=List[ExchangeSymbolRead])
async def list_symbols(exchange_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ExchangeSymbol).where(ExchangeSymbol.exchange_id == exchange_id)
    )
    return result.scalars().all()

# ----------------------------------------------------------------
# Exchange Limits (read-only)
# ----------------------------------------------------------------
@router.get("/{exchange_id}/limits", response_model=List[ExchangeLimitRead])
async def list_limits(exchange_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ExchangeLimit).where(ExchangeLimit.exchange_id == exchange_id)
    )
    return result.scalars().all()

# ----------------------------------------------------------------
# Exchange Fees (read-only)
# ----------------------------------------------------------------
@router.get("/{exchange_id}/fees", response_model=List[ExchangeFeeRead])
async def list_fees(exchange_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ExchangeFee).where(ExchangeFee.exchange_id == exchange_id)
    )
    return result.scalars().all()

# ----------------------------------------------------------------
# Exchange Status History (read-only)
# ----------------------------------------------------------------
@router.get("/{exchange_id}/history", response_model=List[ExchangeStatusHistoryRead])
async def list_status_history(exchange_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ExchangeStatusHistory)
        .where(ExchangeStatusHistory.exchange_id == exchange_id)
        .order_by(ExchangeStatusHistory.created_at.desc())
    )
    return result.scalars().all()
