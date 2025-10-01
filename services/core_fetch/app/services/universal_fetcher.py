import uuid
import logging
from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

import httpx
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from common.deps.session import SessionLocal
from common.models import (
    Exchange,
    ExchangeSymbol,
    ExchangeLimit,
    ExchangeStatusHistory,
    ExchangeFee,
)
from common.models.markethistory import PriceHistory

log = logging.getLogger(__name__)

# =========================
# fetch_and_store_price
# =========================
async def fetch_and_store_price(exchange: str, symbol: str) -> None:
    """
    Fetch latest price for a given symbol from an exchange and store in DB.
    Expects `symbol` as the exchange's symbol code (e.g. "BTCUSDT" for Binance or "XXBTZUSD" for Kraken).
    Saves PriceHistory.symbol as UUID (FK -> exchange_symbols.id).
    Also logs event into ExchangeStatusHistory.
    """
    ex_code = exchange.upper()

    try:
        price: Optional[float] = None

        # ---- Binance ----
        if ex_code == "BINANCE":
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                price = float(data["price"])

        # ---- Kraken ----
        elif ex_code == "KRAKEN":
            url = f"https://api.kraken.com/0/public/Ticker?pair={symbol}"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                result = data.get("result", {})
                if not result:
                    raise ValueError(f"No ticker data for {symbol} from Kraken")
                ticker = list(result.values())[0]
                price = float(ticker["c"][0])  # last trade price

        else:
            log.warning(f"❌ fetch_and_store_price not implemented for {exchange}")
            return

        if price is None:
            raise ValueError(f"No price received for {exchange}:{symbol}")

        # ---- Save to DB ----
        async with SessionLocal() as session:
            # 1) lookup exchange_id
            exch = await session.execute(
                select(Exchange.id).where(Exchange.code == ex_code)
            )
            exchange_id = exch.scalar_one_or_none()
            if not exchange_id:
                raise ValueError(f"Exchange {exchange} not found in DB")

            # 2) lookup symbol UUID
            sym = await session.execute(
                select(ExchangeSymbol.id).where(
                    ExchangeSymbol.exchange_id == exchange_id,
                    (ExchangeSymbol.symbol_id == symbol) | (ExchangeSymbol.symbol == symbol),
                )
            )
            symbol_uuid = sym.scalar_one_or_none()
            if not symbol_uuid:
                raise ValueError(f"Symbol {symbol} not found in DB for {exchange}")

            # 3) write price history
            session.add(
                PriceHistory(
                    timestamp=datetime.now(timezone.utc),
                    exchange_id=exchange_id,
                    symbol=symbol_uuid,
                    price=price,
                )
            )

            # 4) log ok event
            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="price_fetch",
                    status="ok",
                    message=f"Fetched {symbol}={price}",
                )
            )

            await session.commit()

        log.info(f"✅ Stored price {symbol}={price} ({exchange}) in DB")

    except Exception as e:
        log.exception(f"❌ Error fetching price for {exchange}:{symbol}: {e}")

        # ❌ log error into ExchangeStatusHistory
        async with SessionLocal() as session:
            exch = await session.execute(
                select(Exchange.id).where(Exchange.code == ex_code)
            )
            exchange_id = exch.scalar_one_or_none()

            if exchange_id:
                session.add(
                    ExchangeStatusHistory(
                        exchange_id=exchange_id,
                        event="price_fetch",
                        status="error",
                        message=str(e),
                    )
                )
                await session.commit()
# =========================
# refresh_symbols
# =========================
async def refresh_symbols(client: Dict[str, Any], exchange_id: uuid.UUID) -> None:
    """
    Pull symbols from exchange and upsert into exchange_symbols.
    Uniqueness: (exchange_id, symbol_id [exchange-level string ID]).
    """
    log.info(f"🔄 [START] refresh_symbols for {client['exchange_code']}")
    symbols: List[Dict[str, Any]] = []

    try:
        ex_code = client["exchange_code"].upper()

        # ---- Binance ----
        if ex_code == "BINANCE":
            url = "/api/v3/exchangeInfo"
            resp = await client["http"].get(url)
            data = resp.json()

            for s in data.get("symbols", []):
                if s.get("status") != "TRADING":
                    continue

                filters = {f["filterType"]: f for f in s.get("filters", [])}

                min_notional = None
                max_notional = None
                if "MIN_NOTIONAL" in filters:
                    min_notional = filters["MIN_NOTIONAL"].get("minNotional")
                elif "NOTIONAL" in filters:
                    min_notional = filters["NOTIONAL"].get("minNotional")
                    max_notional = filters["NOTIONAL"].get("maxNotional")

                sym_row = dict(
                    exchange_id=exchange_id,
                    symbol_id=s["symbol"],                           # біржовий рядковий ID (e.g. "BTCUSDT")
                    symbol=f"{s['baseAsset']}/{s['quoteAsset']}",    # людиночитний
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
                )
                symbols.append(sym_row)

        # ---- Kraken ----
        elif ex_code == "KRAKEN":
            url = "/0/public/AssetPairs"
            resp = await client["http"].get(url)
            data = resp.json()

            for key, s in data.get("result", {}).items():
                lot_decimals = int(s.get("lot_decimals", 0))
                pair_decimals = int(s.get("pair_decimals", lot_decimals))

                # Numeric-типи бажано як Decimal/str (сумісно з Numeric у моделі)
                step_size: Optional[str] = None
                tick_size: Optional[str] = None
                if lot_decimals:
                    step_size = f"1e-{lot_decimals}"
                if pair_decimals:
                    tick_size = f"1e-{pair_decimals}"

                min_qty = s.get("ordermin")
                min_qty = str(Decimal(min_qty)) if min_qty else None

                sym_row = dict(
                    exchange_id=exchange_id,
                    symbol_id=key,                                      # біржовий рядковий ID Kraken (e.g. "XXBTZUSD")
                    symbol=s.get("wsname") or s.get("altname") or key,  # людиночитний
                    base_asset=s.get("base"),
                    quote_asset=s.get("quote"),
                    status="TRADING",
                    type="spot",
                    base_precision=s.get("pair_decimals"),
                    quote_precision=s.get("lot_decimals"),
                    step_size=step_size,
                    tick_size=tick_size,
                    min_qty=min_qty,
                    max_qty=None,
                    min_notional=None,
                    max_notional=None,
                    filters=s,
                )
                symbols.append(sym_row)

        else:
            log.warning(f"❌ refresh_symbols не реалізовано для {client['exchange_code']}")
            return

        # ---- Upsert into DB ----
        async with SessionLocal() as session:
            for sym in symbols:
                # не оновлюємо ключі у set_: exchange_id, symbol_id
                set_fields = {k: v for k, v in sym.items() if k not in ("exchange_id", "symbol_id")}
                set_fields["fetched_at"] = func.now()

                stmt = (
                    insert(ExchangeSymbol)
                    .values(**sym)
                    .on_conflict_do_update(
                        index_elements=["exchange_id", "symbol_id"],
                        set_=set_fields,
                    )
                )
                await session.execute(stmt)

            await session.execute(
                update(Exchange)
                .where(Exchange.id == exchange_id)
                .values(
                    last_symbols_refresh_at=func.now(),
                    last_filters_refresh_at=func.now(),
                )
            )

            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="symbols_refresh",
                    status="ok",
                    message=f"{len(symbols)} symbols оновлено/додано",
                )
            )

            await session.commit()

        log.info(f"✅ [DONE] {len(symbols)} symbols оновлено/додано")

    except Exception as e:
        log.exception(f"❌ refresh_symbols error: {e}")
        async with SessionLocal() as session:
            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="symbols_refresh",
                    status="error",
                    message=str(e),
                )
            )
            await session.commit()
# =========================
# refresh_limits
# =========================
async def refresh_limits(client: Dict[str, Any], exchange_id: uuid.UUID) -> None:
    """
    Upsert exchange-wide rate limits into exchange_limits.
    Uniqueness: (exchange_id, limit_type, interval_unit, interval_num).
    """
    log.info(f"🔄 [START] refresh_limits for {client['exchange_code']}")
    limits: List[Dict[str, Any]] = []

    try:
        ex_code = client["exchange_code"].upper()

        if ex_code == "BINANCE":
            url = "/api/v3/exchangeInfo"
            resp = await client["http"].get(url)
            data = resp.json()

            for rl in data.get("rateLimits", []):
                limits.append(
                    dict(
                        exchange_id=exchange_id,
                        limit_type=rl["rateLimitType"],
                        interval_unit=rl["interval"],
                        interval_num=rl["intervalNum"],
                        limit=rl["limit"],
                        raw_json=rl,
                    )
                )

        elif ex_code == "KRAKEN":
            limits.append(
                dict(
                    exchange_id=exchange_id,
                    limit_type="REQUEST_WEIGHT",
                    interval_unit="SECOND",
                    interval_num=1,
                    limit=15,
                    raw_json={"docs": "https://support.kraken.com/..."},
                )
            )

        async with SessionLocal() as session:
            for lim in limits:
                # не оновлюємо ключі у set_
                set_fields = {
                    "limit": lim["limit"],
                    "raw_json": lim["raw_json"],
                    "fetched_at": func.now(),
                }
                stmt = (
                    insert(ExchangeLimit)
                    .values(**lim)
                    .on_conflict_do_update(
                        index_elements=[
                            "exchange_id",
                            "limit_type",
                            "interval_unit",
                            "interval_num",
                        ],
                        set_=set_fields,
                    )
                )
                await session.execute(stmt)

            await session.execute(
                update(Exchange)
                .where(Exchange.id == exchange_id)
                .values(last_limits_refresh_at=func.now())
            )

            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="limits_refresh",
                    status="ok",
                    message=f"{len(limits)} limits оновлено/додано",
                )
            )

            await session.commit()

        log.info(f"✅ [DONE] {len(limits)} limits оновлено/додано")

    except Exception as e:
        log.exception(f"❌ refresh_limits error: {e}")
        async with SessionLocal() as session:
            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="limits_refresh",
                    status="error",
                    message=str(e),
                )
            )
            await session.commit()
# =========================
# refresh_fees
# =========================
async def refresh_fees(client: Dict[str, Any], exchange_id: uuid.UUID) -> None:
    """
    Upsert fees into exchange_fees.
    Якщо use_service_symbol = true → всі комісії пишемо в один сервісний символ.
    Інакше працюємо як зараз (per-symbol).
    """
    log.info(f"🔄 [START] refresh_fees for {client['exchange_code']}")
    fees_to_insert: List[Dict[str, Any]] = []

    try:
        async with SessionLocal() as session:
            exch = await session.execute(
                select(Exchange.use_service_symbol).where(Exchange.id == exchange_id)
            )
            use_service = exch.scalar_one()

        ex_code = client["exchange_code"].upper()

        # ---------------- BINANCE ----------------
        if ex_code == "BINANCE":
            url = "/api/v3/account"
            resp = await client["http"].get(url)
            data = resp.json()
            maker = float(data.get("makerCommission", 10)) / 10000
            taker = float(data.get("takerCommission", 10)) / 10000

            if use_service:
                async with SessionLocal() as session:
                    service_id = await ensure_service_symbol(session, exchange_id)
                    await session.commit()
                fees_to_insert.append(
                    dict(
                        exchange_id=exchange_id,
                        symbol_id=service_id,
                        volume_threshold=Decimal(0),
                        maker_fee=Decimal(maker),
                        taker_fee=Decimal(taker),
                    )
                )
            else:
                # логіка як у Kraken: можна робити на всі символи (але Binance не віддає fees по символах)
                # тоді залишаємо один запис з symbol_id=None (fallback)
                fees_to_insert.append(
                    dict(
                        exchange_id=exchange_id,
                        symbol_id=None,
                        volume_threshold=Decimal(0),
                        maker_fee=Decimal(maker),
                        taker_fee=Decimal(taker),
                    )
                )

        # ---------------- KRAKEN ----------------
        elif ex_code == "KRAKEN":
            url = "/0/public/AssetPairs"
            resp = await client["http"].get(url)
            data = resp.json()

            async with SessionLocal() as session:
                for key, s in data.get("result", {}).items():
                    symbol_obj = await session.execute(
                        select(ExchangeSymbol.id).where(
                            ExchangeSymbol.exchange_id == exchange_id,
                            ExchangeSymbol.symbol_id == key,
                        )
                    )
                    symbol_uuid = symbol_obj.scalar_one_or_none()

                    if not symbol_uuid:
                        # створюємо символ якщо немає
                        lot_decimals = int(s.get("lot_decimals", 0))
                        pair_decimals = int(s.get("pair_decimals", lot_decimals))
                        step_size = f"1e-{lot_decimals}" if lot_decimals else None
                        tick_size = f"1e-{pair_decimals}" if pair_decimals else None
                        min_qty = s.get("ordermin")
                        min_qty = str(Decimal(min_qty)) if min_qty else None

                        new_symbol = dict(
                            exchange_id=exchange_id,
                            symbol_id=key,
                            symbol=s.get("wsname") or s.get("altname") or key,
                            base_asset=s.get("base"),
                            quote_asset=s.get("quote"),
                            status="TRADING",
                            type="spot",
                            base_precision=s.get("pair_decimals"),
                            quote_precision=s.get("lot_decimals"),
                            step_size=step_size,
                            tick_size=tick_size,
                            min_qty=min_qty,
                            max_qty=None,
                            min_notional=None,
                            max_notional=None,
                            filters=s,
                        )

                        stmt = (
                            insert(ExchangeSymbol)
                            .values(**new_symbol)
                            .on_conflict_do_update(
                                index_elements=["exchange_id", "symbol_id"],
                                set_={**{k: v for k, v in new_symbol.items() if k not in ("exchange_id", "symbol_id")},
                                      "fetched_at": func.now()}
                            )
                            .returning(ExchangeSymbol.id)
                        )
                        res = await session.execute(stmt)
                        symbol_uuid = res.scalar_one()

                    fees = s.get("fees", [])
                    fees_maker = s.get("fees_maker", [])

                    for idx, level in enumerate(fees):
                        volume, taker = level
                        maker = fees_maker[idx][1] if idx < len(fees_maker) else None

                        fees_to_insert.append(
                            dict(
                                exchange_id=exchange_id,
                                symbol_id=symbol_uuid,
                                volume_threshold=Decimal(volume),
                                maker_fee=Decimal(maker) if maker is not None else None,
                                taker_fee=Decimal(taker),
                            )
                        )

        # ---------------- SAVE ----------------
        async with SessionLocal() as session:
            for fee in fees_to_insert:
                stmt = (
                    insert(ExchangeFee)
                    .values(**fee)
                    .on_conflict_do_update(
                        index_elements=["exchange_id", "symbol_id", "volume_threshold"],
                        set_={
                            "volume_threshold": fee["volume_threshold"],
                            "maker_fee": fee["maker_fee"],
                            "taker_fee": fee["taker_fee"],
                            "fetched_at": func.now(),
                        },
                    )
                )
                await session.execute(stmt)

            await session.execute(
                update(Exchange).where(Exchange.id == exchange_id).values(
                    last_fees_refresh_at=func.now()
                )
            )

            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="fees_refresh",
                    status="ok",
                    message=f"{len(fees_to_insert)} fees оновлено/додано",
                )
            )

            await session.commit()

        log.info(f"✅ [DONE] {len(fees_to_insert)} fees оновлено/додано")

    except Exception as e:
        log.exception(f"❌ refresh_fees error: {e}")
        async with SessionLocal() as session:
            session.add(
                ExchangeStatusHistory(
                    exchange_id=exchange_id,
                    event="fees_refresh",
                    status="error",
                    message=str(e),
                )
            )
            await session.commit()

async def ensure_service_symbol(session: AsyncSession, exchange_id: uuid.UUID) -> uuid.UUID:
    """Знаходить або створює сервісний символ (__SERVICE__) для біржі."""
    res = await session.execute(
        select(ExchangeSymbol.id).where(
            ExchangeSymbol.exchange_id == exchange_id,
            ExchangeSymbol.symbol_id == "__SERVICE__"
        )
    )
    service_id = res.scalar_one_or_none()

    if service_id:
        return service_id

    stmt = (
        insert(ExchangeSymbol)
        .values(
            exchange_id=exchange_id,
            symbol_id="__SERVICE__",
            symbol="SERVICE",
            base_asset="-",
            quote_asset="-",
            status="SERVICE",
            type="service",
            is_active=True,
            filters={}
        )
        .returning(ExchangeSymbol.id)
    )
    res = await session.execute(stmt)
    return res.scalar_one()
