from fastapi import APIRouter, HTTPException
import httpx
from common.deps.config import CoreAdminSettings
from common.schemas.config import (
    SettingCreate, SettingUpdate,
    TimeframeSchema,
    CommandSchema,
    GroupIconSchema,
    ReasonCodeSchema,
    TradeProfileSchema,
    TradeConditionSchema
)


settings = CoreAdminSettings()
router = APIRouter(prefix="/config", tags=["config"])

BASE_URL = settings.CONFIG_BASE_URL.rstrip("/")


async def forward_request(method: str, path: str, data: dict | None = None):
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.request(method, url, json=data)
            resp.raise_for_status()
            if resp.headers.get("content-type", "").startswith("application/json"):
                return resp.json()
            if not resp.text:
                return {"status": resp.status_code}
            return {"raw": resp.text}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

# -------- Settings CRUD --------
@router.get("/settings/{service_name}")
async def list_settings(service_name: str):
    return await forward_request("GET", f"/settings/{service_name}")

@router.post("/settings")
async def create_setting(data: SettingCreate):
    return await forward_request("POST", "/settings", data.dict())

@router.put("/settings/{setting_id}")
async def update_setting(setting_id: str, data: SettingUpdate):
    return await forward_request("PUT", f"/settings/{setting_id}", data.dict())

@router.delete("/settings/{setting_id}")
async def delete_setting(setting_id: str):
    return await forward_request("DELETE", f"/settings/{setting_id}")

from fastapi import APIRouter, HTTPException
import httpx
from common.deps.config import CoreAdminSettings
from common.schemas.config import (
    SettingCreate, SettingUpdate,
    TimeframeSchema,
    CommandSchema,
    GroupIconSchema,
    ReasonCodeSchema,
    TradeProfileSchema,
    TradeConditionSchema,
)

settings = CoreAdminSettings()
router = APIRouter(prefix="/config", tags=["config"])

BASE_URL = settings.CONFIG_BASE_URL.rstrip("/")


async def forward_request(method: str, path: str, data: dict | None = None):
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.request(method, url, json=data)
            resp.raise_for_status()
            if resp.headers.get("content-type", "").startswith("application/json"):
                return resp.json()
            if not resp.text:
                return {"status": resp.status_code}
            return {"raw": resp.text}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

# -------- Timeframes --------
@router.get("/timeframes")
async def list_timeframes():
    return await forward_request("GET", "/timeframes")

@router.post("/timeframes")
async def create_timeframe(item: TimeframeSchema):
    return await forward_request("POST", "/timeframes", item.dict())

@router.put("/timeframes/{code}")
async def update_timeframe(code: str, item: TimeframeSchema):
    return await forward_request("PUT", f"/timeframes/{code}", item.dict())

@router.delete("/timeframes/{code}")
async def delete_timeframe(code: str):
    return await forward_request("DELETE", f"/timeframes/{code}")


# -------- Commands --------
@router.get("/commands")
async def list_commands():
    return await forward_request("GET", "/commands")

@router.post("/commands")
async def create_command(item: CommandSchema):
    return await forward_request("POST", "/commands", item.dict())

@router.put("/commands/{command_id}")
async def update_command(command_id: int, item: CommandSchema):
    return await forward_request("PUT", f"/commands/{command_id}", item.dict())

@router.delete("/commands/{command_id}")
async def delete_command(command_id: int):
    return await forward_request("DELETE", f"/commands/{command_id}")


# -------- Reasons --------
@router.get("/reasons")
async def list_reasons():
    return await forward_request("GET", "/reasons")

@router.post("/reasons")
async def create_reason(item: ReasonCodeSchema):
    return await forward_request("POST", "/reasons", item.dict())

@router.put("/reasons/{code}")
async def update_reason(code: str, item: ReasonCodeSchema):
    return await forward_request("PUT", f"/reasons/{code}", item.dict())

@router.delete("/reasons/{code}")
async def delete_reason(code: str):
    return await forward_request("DELETE", f"/reasons/{code}")


# -------- Trade Profiles --------
@router.get("/trade-profiles")
async def list_trade_profiles():
    return await forward_request("GET", "/trade-profiles")

@router.post("/trade-profiles")
async def create_trade_profile(item: TradeProfileSchema):
    return await forward_request("POST", "/trade-profiles", item.dict())

@router.put("/trade-profiles/{profile_id}")
async def update_trade_profile(profile_id: int, item: TradeProfileSchema):
    return await forward_request("PUT", f"/trade-profiles/{profile_id}", item.dict())

@router.delete("/trade-profiles/{profile_id}")
async def delete_trade_profile(profile_id: int):
    return await forward_request("DELETE", f"/trade-profiles/{profile_id}")


# -------- Trade Conditions --------
@router.get("/trade-conditions")
async def list_trade_conditions():
    return await forward_request("GET", "/trade-conditions")

@router.post("/trade-conditions")
async def create_trade_condition(item: TradeConditionSchema):
    return await forward_request("POST", "/trade-conditions", item.dict())

@router.put("/trade-conditions/{condition_id}")
async def update_trade_condition(condition_id: int, item: TradeConditionSchema):
    return await forward_request("PUT", f"/trade-conditions/{condition_id}", item.dict())

@router.delete("/trade-conditions/{condition_id}")
async def delete_trade_condition(condition_id: int):
    return await forward_request("DELETE", f"/trade-conditions/{condition_id}")


# -------- Group Icons --------
@router.get("/group-icons")
async def list_group_icons():
    return await forward_request("GET", "/group-icons")

@router.post("/group-icons")
async def create_group_icon(item: GroupIconSchema):
    return await forward_request("POST", "/group-icons", item.dict())

@router.put("/group-icons/{group_name}")
async def update_group_icon(group_name: str, item: GroupIconSchema):
    return await forward_request("PUT", f"/group-icons/{group_name}", item.dict())

@router.delete("/group-icons/{group_name}")
async def delete_group_icon(group_name: str):
    return await forward_request("DELETE", f"/group-icons/{group_name}")