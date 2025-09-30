from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from common.models.exchanges import (
    Exchange, ExchangeCredential, ExchangeSymbol,
    ExchangeLimit, ExchangeStatusHistory, ExchangeFee
)
from common.models.users import User

async def get_dashboard_stats(session: AsyncSession):
    # 1) Біржі (active / inactive)
    q_exchanges_active = await session.execute(
        select(func.count()).select_from(Exchange).where(Exchange.is_active == True)
    )
    q_exchanges_inactive = await session.execute(
        select(func.count()).select_from(Exchange).where(Exchange.is_active == False)
    )
    exchanges = {
        "active": q_exchanges_active.scalar_one(),
        "inactive": q_exchanges_inactive.scalar_one(),
    }

    # 2) Кількість ExchangeCredential (усіх)
    q_creds = await session.execute(select(func.count()).select_from(ExchangeCredential))
    service_accounts = q_creds.scalar_one()

    # 3) Symbols per exchange (рахуємо активні символи)
    q_symbols = await session.execute(
        select(Exchange.name, func.count(ExchangeSymbol.id))
        .join(ExchangeSymbol, ExchangeSymbol.exchange_id == Exchange.id)
        .where(ExchangeSymbol.is_active == True)
        .group_by(Exchange.name)
    )
    symbols_per_exchange = {name: count for name, count in q_symbols.all()}

    # 4) "Fetch results" замінимо на агрегацію по ExchangeStatusHistory (by event)
    q_fetch_by_event = await session.execute(
        select(
            ExchangeStatusHistory.event,
            func.sum(case((ExchangeStatusHistory.status == "success", 1), else_=0)).label("success"),
            func.sum(case((ExchangeStatusHistory.status != "success", 1), else_=0)).label("fail"),
        ).group_by(ExchangeStatusHistory.event)
    )
    fetch_by_type = [
        {"type": event, "success": success, "fail": fail}
        for event, success, fail in q_fetch_by_event.all()
    ]

    overall_success = sum(row["success"] for row in fetch_by_type)
    overall_fail = sum(row["fail"] for row in fetch_by_type)
    fetch_overall = [
        {"type": "Success", "value": overall_success},
        {"type": "Fail", "value": overall_fail},
    ]

    # 5) Users active / inactive
    q_users_active = await session.execute(
        select(func.count()).select_from(User).where(User.is_active == True)
    )
    q_users_inactive = await session.execute(
        select(func.count()).select_from(User).where(User.is_active == False)
    )
    users = [
        {"status": "Active", "value": q_users_active.scalar_one()},
        {"status": "Inactive", "value": q_users_inactive.scalar_one()},
    ]

    return {
        "exchanges": exchanges,
        "serviceAccounts": service_accounts,
        "symbolsPerExchange": symbols_per_exchange,
        "fetchResults": {
            "overall": fetch_overall,
            "byType": fetch_by_type,
        },
        "users": users,
    }
