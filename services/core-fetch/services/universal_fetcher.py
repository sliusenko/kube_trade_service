import logging
import requests
from decimal import Decimal
from sqlalchemy import delete, update
from sqlalchemy.sql import func
from core_fetch.db.models import ExchangeSymbol, Exchange, ExchangeLimit, ExchangeStatusHistory
from core_fetch.db.session import SessionLocal

async def refresh_symbols(client, exchange_id):
    logging.info(f"🔄 [START] refresh_symbols for {client['exchange_code']}")

    symbols = []

    # ---- Binance ----
    if client["exchange_code"] == "BINANCE":
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

            symbols.append(dict(
                exchange_id=exchange_id,
                symbol=s["symbol"],
                base_asset=s["baseAsset"],
                quote_asset=s["quoteAsset"],
                status=s["status"],
                base_precision=s.get("baseAssetPrecision"),
                quote_precision=s.get("quotePrecision"),
                step_size=filters.get("LOT_SIZE", {}).get("stepSize"),
                tick_size=filters.get("PRICE_FILTER", {}).get("tickSize"),
                min_qty=filters.get("LOT_SIZE", {}).get("minQty"),
                max_qty=filters.get("LOT_SIZE", {}).get("maxQty"),
                min_notional=filters.get("MIN_NOTIONAL", {}).get("minNotional"),
                filters=s.get("filters", []),
            ))

    # ---- Kraken ----
    elif client["exchange_code"] == "KRAKEN":
        url = "/0/public/AssetPairs"
        logging.debug(f"📡 Запит до {client['exchange_code']} {url}")
        resp = await client["http"].get(url)
        logging.debug(f"📥 Відповідь {client['exchange_code']} статус={resp.status_code}")
        data = resp.json()

        logging.debug(f"📊 Отримано {len(data.get('result', {}))} symbols від {client['exchange_code']}")

        for key, s in data.get("result", {}).items():
            base = s.get("base")
            quote = s.get("quote")
            symbols.append(dict(
                exchange_id=exchange_id,
                symbol=key,
                base_asset=base,
                quote_asset=quote,
                status="TRADING",
                base_precision=s.get("pair_decimals"),
                quote_precision=s.get("lot_decimals"),
                step_size=None,
                tick_size=None,
                min_qty=None,
                max_qty=None,
                min_notional=None,
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
        session.add_all([ExchangeSymbol(**sym) for sym in symbols])
        await session.commit()

        await session.execute(
            update(Exchange)
            .where(Exchange.id == exchange_id)
            .values(last_symbols_refresh_at=func.now())
        )
    logging.info(f"✅ [DONE] {len(symbols)} symbols збережено для {client['exchange_code']}")

# ---------------------------
# refresh_filters
# ---------------------------
async def refresh_filters(client, exchange_id):
    logging.info(f"🔄 [START] refresh_filters for {client['exchange_code']}")

    try:
        filters_data = []

        if client["exchange_code"].lower() == "binance":
            # Binance exchangeInfo
            info = client["api"].get_exchange_info()
            for s in info["symbols"]:

                lot_filter = next((f for f in s["filters"] if f["filterType"] == "LOT_SIZE"), None)
                price_filter = next((f for f in s["filters"] if f["filterType"] == "PRICE_FILTER"), None)

                if lot_filter:
                    filters_data.append({
                        "exchange_id": exchange_id,
                        "limit_type": "LOT_SIZE",
                        "interval_unit": "symbol",
                        "interval_num": 1,
                        "limit": float(lot_filter["minQty"]),
                        "raw_json": {
                            "min_qty": lot_filter["minQty"],
                            "max_qty": lot_filter["maxQty"],
                            "step_size": lot_filter["stepSize"],
                            "tick_size": float(price_filter["tickSize"]) if price_filter else None
                        },
                        "fetched_at": func.now()
                    })

        elif client["exchange_code"].lower() == "kraken":
            # Kraken AssetPairs
            res = requests.get("https://api.kraken.com/0/public/AssetPairs")
            res.raise_for_status()
            data = res.json()["result"]

            for _, item in data.items():
                altname = item.get("altname")
                if not altname:
                    continue

                lot_decimals = int(item["lot_decimals"])
                step_size = Decimal(f"1e-{lot_decimals}")
                min_qty = Decimal(item["ordermin"])
                pair_decimals = int(item.get("pair_decimals", lot_decimals))
                tick_size = Decimal(f"1e-{pair_decimals}")

                filters_data.append({
                    "exchange_id": exchange_id,
                    "limit_type": "LOT_SIZE",
                    "interval_unit": "symbol",
                    "interval_num": 1,
                    "limit": float(min_qty),
                    "raw_json": {
                        "min_qty": str(min_qty),
                        "step_size": str(step_size),
                        "tick_size": str(tick_size)
                    },
                    "fetched_at": func.now()
                })

        # --- DB update ---
        async with SessionLocal() as session:
            await session.execute(delete(ExchangeLimit).where(ExchangeLimit.exchange_id == exchange_id))
            if filters_data:
                session.add_all([ExchangeLimit(**f) for f in filters_data])

            await session.execute(
                update(Exchange)
                .where(Exchange.id == exchange_id)
                .values(last_filters_refresh_at=func.now())
            )

            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="filters_refresh",
                status="ok",
                message=f"{len(filters_data)} filters збережено"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] filters для {client['exchange_code']} оновлено")

    except Exception as e:
        logging.exception(f"❌ refresh_filters error for {client['exchange_code']}: {e}")
        async with SessionLocal() as session:
            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="filters_refresh",
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
        limits_data = []

        if client["exchange_code"].lower() == "binance":
            # Тут можна використати client["api"].get_exchange_info()
            # і витягнути наприклад MIN_NOTIONAL
            info = client["api"].get_exchange_info()
            for s in info["symbols"]:
                min_notional = next((f for f in s["filters"] if f["filterType"] == "MIN_NOTIONAL"), None)
                if min_notional:
                    limits_data.append({
                        "exchange_id": exchange_id,
                        "limit_type": "MIN_NOTIONAL",
                        "interval_unit": "symbol",
                        "interval_num": 1,
                        "limit": float(min_notional["minNotional"]),
                        "raw_json": min_notional,
                        "fetched_at": func.now()
                    })

        elif client["exchange_code"].lower() == "kraken":
            # У Kraken можна використати поля costmin (мінімальна вартість угоди)
            res = requests.get("https://api.kraken.com/0/public/AssetPairs")
            res.raise_for_status()
            data = res.json()["result"]

            for _, item in data.items():
                altname = item.get("altname")
                if not altname:
                    continue
                costmin = item.get("costmin")
                if costmin:
                    limits_data.append({
                        "exchange_id": exchange_id,
                        "limit_type": "MIN_NOTIONAL",
                        "interval_unit": "symbol",
                        "interval_num": 1,
                        "limit": float(costmin),
                        "raw_json": item,
                        "fetched_at": func.now()
                    })

        # --- DB update ---
        async with SessionLocal() as session:
            await session.execute(delete(ExchangeLimit).where(ExchangeLimit.exchange_id == exchange_id))
            if limits_data:
                session.add_all([ExchangeLimit(**l) for l in limits_data])

            await session.execute(
                update(Exchange)
                .where(Exchange.id == exchange_id)
                .values(last_limits_refresh_at=func.now())
            )

            session.add(ExchangeStatusHistory(
                exchange_id=exchange_id,
                event="limits_refresh",
                status="ok",
                message=f"{len(limits_data)} limits збережено"
            ))

            await session.commit()

        logging.info(f"✅ [DONE] limits для {client['exchange_code']} оновлено")

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