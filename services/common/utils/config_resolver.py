import os
import logging
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from common.models.config import Setting

log = logging.getLogger(__name__)

class ConfigResolver:
    """
    Пріоритет:
    1. Env з Deployment (k8s)
    2. settings (таблиця в Postgres)
    3. Defaults із BaseSettings
    """

    def __init__(self, service_name: str, defaults: dict[str, Any]):
        self.service_name = service_name
        self.defaults = defaults

    async def get(self, session: AsyncSession, key: str) -> Optional[str]:
        # 1) Env
        if key in os.environ:
            return os.environ[key]

        # 2) settings DB
        q = select(Setting.value).where(
            Setting.service_name == self.service_name,
            Setting.key == key
        )
        result = await session.execute(q)
        db_val = result.scalar_one_or_none()
        if db_val is not None:
            return db_val

        # 3) Defaults
        return self.defaults.get(key)

    async def get_int(self, session: AsyncSession, key: str) -> Optional[int]:
        val = await self.get(session, key)
        return int(val) if val is not None else None

    async def get_float(self, session: AsyncSession, key: str) -> Optional[float]:
        val = await self.get(session, key)
        return float(val) if val is not None else None

    async def get_dict(self, session: AsyncSession, key: str) -> Optional[dict]:
        import json
        val = await self.get(session, key)
        if val is None:
            return None
        if isinstance(val, dict):
            return val
        try:
            return json.loads(val)
        except Exception:
            log.warning("⚠️ ConfigResolver: key=%s не вдалося розпарсити dict", key)
            return None
