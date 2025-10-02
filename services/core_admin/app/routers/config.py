from fastapi import APIRouter, HTTPException
import httpx
from common.deps.config import CoreAdminSettings

settings = CoreAdminSettings()
router = APIRouter(prefix="/config", tags=["config"])

BASE_URL = settings.CONFIG_BASE_URL.rstrip("/")


async def forward_request(method: str, path: str, data: dict | None = None):
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.request(method, url, json=data)
            resp.raise_for_status()
            # Якщо є JSON
            if resp.headers.get("content-type", "").startswith("application/json"):
                return resp.json()
            # Якщо немає тіла, але є статус
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
async def create_setting(data: dict):
    return await forward_request("POST", "/settings", data)

@router.put("/settings/{setting_id}")
async def update_setting(setting_id: str, data: dict):
    return await forward_request("PUT", f"/settings/{setting_id}", data)

@router.delete("/settings/{setting_id}")
async def delete_setting(setting_id: str):
    return await forward_request("DELETE", f"/settings/{setting_id}")

# -------- Timeframes --------
@router.get("/timeframes")
async def list_timeframes():
    return await forward_request("GET", "/timeframes")

@router.post("/timeframes")
async def create_timeframe(item: dict):
    return await forward_request("POST", "/timeframes", item)

@router.put("/timeframes/{code}")
async def update_timeframe(code: str, item: dict):
    return await forward_request("PUT", f"/timeframes/{code}", item)

@router.delete("/timeframes/{code}")
async def delete_timeframe(code: str):
    return await forward_request("DELETE", f"/timeframes/{code}")


# -------- Commands --------
@router.get("/commands")
async def list_commands():
    return await forward_request("GET", "/commands")

@router.post("/commands")
async def create_command(item: dict):
    return await forward_request("POST", "/commands", item)

@router.put("/commands/{command_id}")
async def update_command(command_id: int, item: dict):
    return await forward_request("PUT", f"/commands/{command_id}", item)

@router.delete("/commands/{command_id}")
async def delete_command(command_id: int):
    return await forward_request("DELETE", f"/commands/{command_id}")


# -------- Reasons --------
@router.get("/reasons")
async def list_reasons():
    return await forward_request("GET", "/reasons")

@router.post("/reasons")
async def create_reason(item: dict):
    return await forward_request("POST", "/reasons", item)

@router.put("/reasons/{code}")
async def update_reason(code: str, item: dict):
    return await forward_request("PUT", f"/reasons/{code}", item)

@router.delete("/reasons/{code}")
async def delete_reason(code: str):
    return await forward_request("DELETE", f"/reasons/{code}")


# -------- Trade Profiles --------
@router.get("/trade-profiles")
async def list_trade_profiles():
    return await forward_request("GET", "/trade-profiles")

@router.post("/trade-profiles")
async def create_trade_profile(item: dict):
    return await forward_request("POST", "/trade-profiles", item)

@router.put("/trade-profiles/{profile_id}")
async def update_trade_profile(profile_id: int, item: dict):
    return await forward_request("PUT", f"/trade-profiles/{profile_id}", item)

@router.delete("/trade-profiles/{profile_id}")
async def delete_trade_profile(profile_id: int):
    return await forward_request("DELETE", f"/trade-profiles/{profile_id}")


# -------- Trade Conditions --------
@router.get("/trade-conditions")
async def list_trade_conditions():
    return await forward_request("GET", "/trade-conditions")

@router.post("/trade-conditions")
async def create_trade_condition(item: dict):
    return await forward_request("POST", "/trade-conditions", item)

@router.put("/trade-conditions/{condition_id}")
async def update_trade_condition(condition_id: int, item: dict):
    return await forward_request("PUT", f"/trade-conditions/{condition_id}", item)

@router.delete("/trade-conditions/{condition_id}")
async def delete_trade_condition(condition_id: int):
    return await forward_request("DELETE", f"/trade-conditions/{condition_id}")


# -------- Group Icons --------
@router.get("/group-icons")
async def list_group_icons():
    return await forward_request("GET", "/group-icons")

@router.post("/group-icons")
async def create_group_icon(item: dict):
    return await forward_request("POST", "/group-icons", item)

@router.put("/group-icons/{group_name}")
async def update_group_icon(group_name: str, item: dict):
    return await forward_request("PUT", f"/group-icons/{group_name}", item)

@router.delete("/group-icons/{group_name}")
async def delete_group_icon(group_name: str):
    return await forward_request("DELETE", f"/group-icons/{group_name}")
