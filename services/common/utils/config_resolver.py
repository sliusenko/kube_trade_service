import os
import json
import logging
from typing import Any, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from common.models.config import Setting

log = logging.getLogger(__name__)

class ConfigResolver:
    """
    Пріоритет:
      1) env (НЕ пустий)
      2) settings (DB) з урахуванням value_type
      3) defaults (передані в конструкторі)
    """

    def __init__(self, service_name: str, defaults: dict[str, Any], extra_service_names: Sequence[str] | None = None):
        # підтримуємо кілька назв (наприклад, core-news і kube-trade-bot-core-news)
        names = [service_name, os.getenv("SERVICE_NAME", "").strip()]
        if extra_service_names:
            names.extend(extra_service_names)
        # унікалізуємо і фільтруємо порожні
        self.service_names = [n for i, n in enumerate(names) if n and n not in names[:i]]
        self.defaults = defaults or {}

    # ---------- internal helpers ----------
    def _env_get(self, key: str) -> Optional[str]:
        val = os.getenv(key)
        if val is None:
            return None
        # Порожній рядок трактуємо як відсутність значення
        return val if val != "" else None
    async def _db_get_raw(self, session: AsyncSession, key: str) -> tuple[Optional[str], Optional[str]]:
        if not self.service_names:
            return None, None
        q = (
            select(Setting.value, Setting.value_type)
            .where(Setting.service_name.in_(self.service_names), Setting.key == key)
            .order_by(Setting.updated_at.desc())
            .limit(1)
        )
        row = (await session.execute(q)).first()
        if not row:
            return None, None
        return row[0], (row[1] or "str")
    def _parse_by_type(self, raw: str, value_type: str) -> Any:
        try:
            vt = (value_type or "str").lower()
            if vt == "int":
                return int(raw)
            if vt == "float":
                return float(raw)
            if vt == "json":
                # пусте значення для json вважаємо як None
                return None if raw == "" else json.loads(raw)
            # "str" або невідомий тип
            return raw
        except Exception:
            log.warning("⚠️ ConfigResolver: не вдалося привести '%s' до типу %s", raw, value_type)
            return None

    # ---------- public API ----------

    async def get(self, session: AsyncSession, key: str) -> Optional[str]:
        # 1) env (не порожній)
        v = self._env_get(key)
        if v is not None:
            return v

        # 2) DB
        raw, vtype = await self._db_get_raw(session, key)
        if raw is not None:
            val = self._parse_by_type(raw, vtype)
            # Якщо тип був не str — все одно get() повертає str
            return str(val) if val is not None else None

        # 3) defaults
        return self.defaults.get(key)
    async def get_int(self, session: AsyncSession, key: str) -> Optional[int]:
        # env
        v = self._env_get(key)
        if v is not None:
            try:
                return int(v)
            except ValueError:
                log.warning("⚠️ ConfigResolver: key=%s має некоректне env '%s' (очікував int)", key, v)
                return None

        # db
        raw, vtype = await self._db_get_raw(session, key)
        if raw is not None:
            val = self._parse_by_type(raw, vtype)
            if isinstance(val, int):
                return val
            try:
                return int(val) if val not in (None, "") else None
            except (ValueError, TypeError):
                log.warning("⚠️ ConfigResolver: key=%s(DB)='%s' не приводиться до int", key, val)
                return None

        # defaults
        dv = self.defaults.get(key)
        try:
            return int(dv) if dv not in (None, "") else None
        except (ValueError, TypeError):
            return None
    async def get_float(self, session: AsyncSession, key: str) -> Optional[float]:
        # env
        v = self._env_get(key)
        if v is not None:
            try:
                return float(v)
            except ValueError:
                log.warning("⚠️ ConfigResolver: key=%s має некоректне env '%s' (очікував float)", key, v)
                return None

        # db
        raw, vtype = await self._db_get_raw(session, key)
        if raw is not None:
            val = self._parse_by_type(raw, vtype)
            if isinstance(val, float | int):
                return float(val)
            try:
                return float(val) if val not in (None, "") else None
            except (ValueError, TypeError):
                log.warning("⚠️ ConfigResolver: key=%s(DB)='%s' не приводиться до float", key, val)
                return None

        # defaults
        dv = self.defaults.get(key)
        try:
            return float(dv) if dv not in (None, "") else None
        except (ValueError, TypeError):
            return None
    async def get_dict(self, session: AsyncSession, key: str) -> Optional[dict]:
        # env
        v = self._env_get(key)
        if v is not None:
            try:
                return json.loads(v)
            except Exception:
                log.warning("⚠️ ConfigResolver: key=%s env не JSON, пропускаю", key)

        # db
        raw, vtype = await self._db_get_raw(session, key)
        if raw is not None:
            val = self._parse_by_type(raw, vtype)
            if isinstance(val, dict):
                return val
            # інколи збережений як str JSON
            try:
                return json.loads(val) if isinstance(val, str) and val != "" else None
            except Exception:
                log.warning("⚠️ ConfigResolver: key=%s(DB) не JSON", key)
                return None

        # defaults
        dv = self.defaults.get(key)
        return dv if isinstance(dv, dict) else None
