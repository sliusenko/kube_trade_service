import logging
import requests
from decimal import Decimal
from sqlalchemy import delete, update, func
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
            logging.debug(f"📡 Запит до {client['exchange_code']} {url}")
            resp = await client["http"].get(url)
            logging.debug(f"📥 Відповідь {client['exchange_code']} статус={resp.status_code}")
            data = resp.json()

            logging.debug(f"📊 Отримано {len(data.get('symbols', []))} symbols від {client['exchange_code']}")

            for s in data.get("symbols", []):
                if s["status"] != "TRADING":
                    logging.debug(f"⏭️ Пропускаю {s['symbol']} (status={s['status']})")
                    continue

                filters = {f["filterType"]: f for f in s.get("filters", [])}

                # ---- min_notional / max_notional ----
                min_notional = None
                max_notional = None

                if "MIN_NOTIONAL" in filters:
                    min_notional = filters["MIN_NOTIONAL"].get("minNotional")
                elif "NOTIONAL" in filters:
                    min_notional = filters["NOTIONAL"].get("minNotional")
                    max_notional = filters["NOTIONAL"].get("maxNotional")

                symbols.append(dict(
                    exchange_id=exchange_id,
                    symbol=s["symbol"],
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
            logging.debug(f"📡 Запит до {client['exchange_code']} {url}")
            resp = await client["http"].get(url)
            logging.debug(f"📥 Відповідь {client['exchange_code']} статус={resp.status_code}")
            data = resp.json()

            logging.debug(f"📊 Отримано {len(data.get('result', {}))} symbols від {client['exchange_code']}")

            for key, s in data.get("result", {}).items():
                base = s.get("base")
                quote = s.get("quote")

                # розрахунок кроків для кількості та ціни
                lot_decimals = int(s.get("lot_decimals", 0))
                step_size = Decimal(f"1e-{lot_decimals}") if lot_decimals else None
                min_qty = Decimal(s.get("ordermin")) if s.get("ordermin") else None
                pair_decimals = int(s.get("pair_decimals", lot_decimals))
                tick_size = Decimal(f"1e-{pair_decimals}") if pair_decimals else None

                symbols.append(dict(
                    exchange_id=exchange_id,
                    symbol=key,
                    base_asset=base,
                    quote_asset=quote,
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

        logging.info(f"📝 Підготовлено {len(symbols)} symbols для {client['exchange_code']} (exchange_id={exchange_id})")

        # ---- Запис у базу ----
        async with SessionLocal() as session:
            logging.debug(f"🗑️ Видаляю старі symbols для exchange_id={exchange_id}")
            await session.execute(
                delete(ExchangeSymbol).where(ExchangeSymbol.exchange_id == exchange_id)
            )

            logging.debug(f"➕ Додаю {len(symbols)} нових symbols у exchange_symbols")
            if symbols:
                session.add_all([ExchangeSymbol(**sym) for sym in symbols])

            # оновлюємо last_symbols_refresh_at + last_filters_refresh_at
            await session.execute(
                update(Exchange)
                .where(Exchange.id == exchange_id)
                .values(
                    last_symbols_refresh_at=func.now(),
                    last_filters_refresh_at=func.now()
                )
            )

            # додаємо запис в ExchangeStatusHistory
            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="symbols_refresh",
                status="ok",
                message=f"{len(symbols)} symbols збережено"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] {len(symbols)} symbols збережено для {client['exchange_code']}")

    except Exception as e:
        logging.exception(f"❌ refresh_symbols error for {client['exchange_code']}: {e}")
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

    try:
        limits = []

        # ---- Binance ----
        if client["exchange_code"].upper() == "BINANCE":
            url = "/api/v3/exchangeInfo"
            logging.debug(f"📡 Запит до {client['exchange_code']} {url}")
            resp = await client["http"].get(url)
            logging.debug(f"📥 Відповідь {client['exchange_code']} статус={resp.status_code}")
            data = resp.json()

            for rl in data.get("rateLimits", []):
                limits.append(dict(
                    exchange_id=exchange_id,
                    limit_type=rl["rateLimitType"],     # REQUEST_WEIGHT, ORDERS
                    interval_unit=rl["interval"],       # SECOND, MINUTE, DAY
                    interval_num=rl["intervalNum"],     # 1, 60, 86400
                    limit=rl["limit"],
                    raw_json=rl,
                ))

        # ---- Kraken ----
        elif client["exchange_code"].upper() == "KRAKEN":
            # Kraken має просту систему лімітів: https://support.kraken.com/hc/en-us/articles/360022635592
            # Їх треба хардкодити або фетчити з довідки, бо через API не віддає
            limits.append(dict(
                exchange_id=exchange_id,
                limit_type="REQUEST_WEIGHT",
                interval_unit="SECOND",
                interval_num=1,
                limit=15,   # приклад: 15 запитів на 3 секунди (можна нормалізувати)
                raw_json={"docs": "https://support.kraken.com/hc/en-us/articles/360022635592"}
            ))

        else:
            logging.warning(f"❌ refresh_limits не реалізовано для {client['exchange_code']}")
            return

        logging.info(f"📝 Підготовлено {len(limits)} limits для {client['exchange_code']} (exchange_id={exchange_id})")

        # ---- Запис у базу ----
        async with SessionLocal() as session:
            logging.debug(f"🗑️ Видаляю старі limits для exchange_id={exchange_id}")
            await session.execute(
                delete(ExchangeLimit).where(ExchangeLimit.exchange_id == exchange_id)
            )

            logging.debug(f"➕ Додаю {len(limits)} нових limits у exchange_limits")
            if limits:
                session.add_all([ExchangeLimit(**lim) for lim in limits])

            # оновлюємо last_limits_refresh_at
            await session.execute(
                update(Exchange)
                .where(Exchange.id == exchange_id)
                .values(last_limits_refresh_at=func.now())
            )

            # додаємо запис в ExchangeStatusHistory
            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="limits_refresh",
                status="ok",
                message=f"{len(limits)} limits збережено"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] {len(limits)} limits збережено для {client['exchange_code']}")

    except Exception as e:
        logging.exception(f"❌ refresh_limits error for {client['exchange_code']}: {e}")
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
        # ---- Binance ----
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

        # ---- Kraken ----
        elif client["exchange_code"].upper() == "KRAKEN":
            url = "/0/public/AssetPairs"
            resp = await client["http"].get(url)
            data = resp.json()

            for key, s in data.get("result", {}).items():
                fees = s.get("fees", [])
                fees_maker = s.get("fees_maker", [])

                # fees = [[volume, taker%], ...]
                # fees_maker = [[volume, maker%], ...]
                for idx, level in enumerate(fees):
                    volume, taker = level
                    maker = fees_maker[idx][1] if idx < len(fees_maker) else None

                    fees_to_insert.append(dict(
                        exchange_id=exchange_id,
                        symbol_id=None,   # тут можна підставити id символу, якщо робиш lookup по key
                        volume_threshold=Decimal(volume),
                        maker_fee=Decimal(maker) if maker is not None else None,
                        taker_fee=Decimal(taker),
                    ))

        else:
            logging.warning(f"❌ refresh_fees не реалізовано для {client['exchange_code']}")
            return

        # ---- Запис у базу ----
        async with SessionLocal() as session:
            logging.debug(f"🗑️ Видаляю старі fees для exchange_id={exchange_id}")
            await session.execute(delete(ExchangeFee).where(ExchangeFee.exchange_id == exchange_id))

            if fees_to_insert:
                session.add_all([ExchangeFee(**f) for f in fees_to_insert])

            await session.execute(
                update(Exchange)
                .where(Exchange.id == exchange_id)
                .values(last_fees_refresh_at=func.now())
            )

            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="fees_refresh",
                status="ok",
                message=f"{len(fees_to_insert)} fees збережено"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] {len(fees_to_insert)} fees збережено для {client['exchange_code']}")

    except Exception as e:
        logging.exception(f"❌ refresh_fees error for {client['exchange_code']}: {e}")
        async with SessionLocal() as session:
            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="fees_refresh",
                status="error",
                message=str(e)
            ))
            await session.commit()
