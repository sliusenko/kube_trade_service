import logging
import requests
from decimal import Decimal
from sqlalchemy import delete, update, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func
from core_fetch.db.models import ExchangeSymbol, Exchange, ExchangeLimit, ExchangeStatusHistory, ExchangeFee
from core_fetch.db.session import SessionLocal
from binance.client import Client as BinanceClient


async def refresh_symbols(client, exchange_id):
    logging.info(f"🔄 [START] refresh_symbols for {client['exchange_code']}")

    symbols = []

    try:
        # ---- Binance ----
        if client["exchange_code"].upper() == "BINANCE":
            url = "/api/v3/exchangeInfo"
            resp = await client["http"].get(url)
            data = resp.json()

            for s in data.get("symbols", []):
                if s["status"] != "TRADING":
                    continue

                filters = {f["filterType"]: f for f in s.get("filters", [])}

                min_notional = None
                max_notional = None
                if "MIN_NOTIONAL" in filters:
                    min_notional = filters["MIN_NOTIONAL"].get("minNotional")
                elif "NOTIONAL" in filters:
                    min_notional = filters["NOTIONAL"].get("minNotional")
                    max_notional = filters["NOTIONAL"].get("maxNotional")

                symbols.append(dict(
                    exchange_id=exchange_id,
                    symbol_id=s["symbol"],       # 👈 унікальний ключ від біржі
                    symbol=f"{s['baseAsset']}/{s['quoteAsset']}",
                    base_asset=s["baseAsset"],
                    quote_asset=s["quoteAsset"],
                    status=s["status"],
                    type="spot",
                    base_precision=s.get("baseAssetPrecision"),
                    quote_precision=s.get("quotePrecision"),
                    step_size=filters.get("LOT_SIZE", {}).get("stepSize"),
                    tick_size=filters.get("PRICE_FILTER", {}).get("tickSize"),
                    min_qty=filters.get("LOT_SIZE", {}).get("minQty"),
                    max_qty=filters.get("LOT_SIZE", {}).get("maxQty"),
                    min_notional=min_notional,
                    max_notional=max_notional,
                    filters=s.get("filters", []),
                ))

        # ---- Kraken ----
        elif client["exchange_code"].upper() == "KRAKEN":
            url = "/0/public/AssetPairs"
            resp = await client["http"].get(url)
            data = resp.json()

            for key, s in data.get("result", {}).items():
                lot_decimals = int(s.get("lot_decimals", 0))
                step_size = Decimal(f"1e-{lot_decimals}") if lot_decimals else None
                min_qty = Decimal(s.get("ordermin")) if s.get("ordermin") else None
                pair_decimals = int(s.get("pair_decimals", lot_decimals))
                tick_size = Decimal(f"1e-{pair_decimals}") if pair_decimals else None

                symbols.append(dict(
                    exchange_id=exchange_id,
                    symbol_id=key,                 # 👈 унікальний ключ Kraken
                    symbol=s.get("wsname") or s.get("altname") or key,
                    base_asset=s.get("base"),
                    quote_asset=s.get("quote"),
                    status="TRADING",
                    type="spot",
                    base_precision=s.get("pair_decimals"),
                    quote_precision=s.get("lot_decimals"),
                    step_size=str(step_size) if step_size else None,
                    tick_size=str(tick_size) if tick_size else None,
                    min_qty=str(min_qty) if min_qty else None,
                    max_qty=None,
                    min_notional=None,
                    max_notional=None,
                    filters=s,
                ))

        else:
            logging.warning(f"❌ refresh_symbols не реалізовано для {client['exchange_code']}")
            return

        async with SessionLocal() as session:
            for sym in symbols:
                stmt = insert(ExchangeSymbol).values(**sym).on_conflict_do_update(
                    index_elements=["exchange_id", "symbol_id"],
                    set_={**sym, "fetched_at": func.now()}
                )
                await session.execute(stmt)

            await session.execute(
                update(Exchange).where(Exchange.id == exchange_id).values(
                    last_symbols_refresh_at=func.now(),
                    last_filters_refresh_at=func.now()
                )
            )

            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="symbols_refresh",
                status="ok",
                message=f"{len(symbols)} symbols оновлено/додано"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] {len(symbols)} symbols оновлено/додано")

    except Exception as e:
        logging.exception(f"❌ refresh_symbols error: {e}")
        async with SessionLocal() as session:
            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="symbols_refresh",
                status="error",
                message=str(e)
            ))
            await session.commit()

# ---------------------------
# refresh_limits
# ---------------------------
async def refresh_limits(client, exchange_id):
    logging.info(f"🔄 [START] refresh_limits for {client['exchange_code']}")

    limits = []
    try:
        if client["exchange_code"].upper() == "BINANCE":
            url = "/api/v3/exchangeInfo"
            resp = await client["http"].get(url)
            data = resp.json()

            for rl in data.get("rateLimits", []):
                limits.append(dict(
                    exchange_id=exchange_id,
                    limit_type=rl["rateLimitType"],
                    interval_unit=rl["interval"],
                    interval_num=rl["intervalNum"],
                    limit=rl["limit"],
                    raw_json=rl,
                ))

        elif client["exchange_code"].upper() == "KRAKEN":
            limits.append(dict(
                exchange_id=exchange_id,
                limit_type="REQUEST_WEIGHT",
                interval_unit="SECOND",
                interval_num=1,
                limit=15,
                raw_json={"docs": "https://support.kraken.com/..."}
            ))

        async with SessionLocal() as session:
            for lim in limits:
                stmt = insert(ExchangeLimit).values(**lim).on_conflict_do_update(
                    index_elements=["exchange_id", "limit_type", "interval_unit", "interval_num"],
                    set_={**lim, "fetched_at": func.now()}
                )
                await session.execute(stmt)

            await session.execute(
                update(Exchange).where(Exchange.id == exchange_id).values(
                    last_limits_refresh_at=func.now()
                )
            )

            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="limits_refresh",
                status="ok",
                message=f"{len(limits)} limits оновлено/додано"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] {len(limits)} limits оновлено/додано")

    except Exception as e:
        logging.exception(f"❌ refresh_limits error: {e}")
        async with SessionLocal() as session:
            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="limits_refresh",
                status="error",
                message=str(e)
            ))
            await session.commit()

async def refresh_fees(client, exchange_id):
    logging.info(f"🔄 [START] refresh_fees for {client['exchange_code']}")
    fees_to_insert = []

    try:
        if client["exchange_code"].upper() == "BINANCE":
            url = "/api/v3/account"
            resp = await client["http"].get(url)
            data = resp.json()
            maker = float(data.get("makerCommission", 10)) / 10000
            taker = float(data.get("takerCommission", 10)) / 10000

            fees_to_insert.append(dict(
                exchange_id=exchange_id,
                symbol_id=None,
                volume_threshold=0,
                maker_fee=maker,
                taker_fee=taker,
            ))

        elif client["exchange_code"].upper() == "KRAKEN":
            url = "/0/public/AssetPairs"
            resp = await client["http"].get(url)
            data = resp.json()

            async with SessionLocal() as session:
                for key, s in data.get("result", {}).items():
                    # 🔎 lookup symbol.id по symbol_id (Kraken key)
                    symbol_obj = await session.execute(
                        select(ExchangeSymbol.id).where(
                            ExchangeSymbol.exchange_id == exchange_id,
                            ExchangeSymbol.symbol_id == key
                        )
                    )
                    symbol_id_db = symbol_obj.scalar_one_or_none()

                    fees = s.get("fees", [])
                    fees_maker = s.get("fees_maker", [])

                    for idx, level in enumerate(fees):
                        volume, taker = level
                        maker = fees_maker[idx][1] if idx < len(fees_maker) else None

                        fees_to_insert.append(dict(
                            exchange_id=exchange_id,
                            symbol_id=symbol_id_db,  # 👈 підставили правильний FK
                            volume_threshold=Decimal(volume),
                            maker_fee=Decimal(maker) if maker is not None else None,
                            taker_fee=Decimal(taker),
                        ))

        async with SessionLocal() as session:
            for fee in fees_to_insert:
                stmt = insert(ExchangeFee).values(**fee).on_conflict_do_update(
                    index_elements=["exchange_id", "symbol_id", "volume_threshold"],
                    set_={**fee, "fetched_at": func.now()}
                )
                await session.execute(stmt)

            await session.execute(
                update(Exchange).where(Exchange.id == exchange_id).values(
                    last_fees_refresh_at=func.now()
                )
            )

            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="fees_refresh",
                status="ok",
                message=f"{len(fees_to_insert)} fees оновлено/додано"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] {len(fees_to_insert)} fees оновлено/додано")

    except Exception as e:
        logging.exception(f"❌ refresh_fees error: {e}")
        async with SessionLocal() as session:
            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="fees_refresh",
                status="error",
                message=str(e)
            ))
            await session.commit()
