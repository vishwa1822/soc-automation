from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from alert_store import get_alerts
from honeytokens.engine_instance import honeytoken_engine
from soar_store import (
    block_ip,
    get_state,
    run_auto_block,
    set_auto_block,
    set_automation,
    set_threshold,
    toggle_playbook,
)

router = APIRouter()


class EnabledBody(BaseModel):
    enabled: bool


class ThresholdBody(BaseModel):
    threshold: int = Field(ge=40, le=95)


class BlockIpBody(BaseModel):
    ip: str
    reason: str = ""


@router.get("/alerts")
def list_alerts():
    return {"alerts": get_alerts()}


@router.get("/soar/dashboard")
def soar_dashboard():
    triggers = honeytoken_engine.get_trigger_history()
    return {
        "alerts": get_alerts(),
        "triggers": triggers if isinstance(triggers, list) else [],
        "soar": get_state(),
    }


@router.get("/soar/state")
def soar_state():
    return get_state()


@router.post("/soar/automation")
def soar_automation(body: EnabledBody):
    set_automation(body.enabled)
    return {"ok": True, "state": get_state()}


@router.post("/soar/auto-block")
def soar_auto_block(body: EnabledBody):
    set_auto_block(body.enabled)
    return {"ok": True, "state": get_state()}


@router.post("/soar/threshold")
def soar_threshold(body: ThresholdBody):
    set_threshold(body.threshold)
    return {"ok": True, "state": get_state()}


@router.post("/soar/block-ip")
def soar_block_ip(body: BlockIpBody):
    ok, message = block_ip(body.ip, body.reason)
    return {"ok": ok, "message": message, "state": get_state()}


@router.post("/soar/auto-block-run")
def soar_auto_block_run():
    blocked, message = run_auto_block()
    return {"ok": True, "blocked": blocked, "message": message, "state": get_state()}


@router.post("/soar/playbook/{playbook_id}/toggle")
def soar_toggle_playbook(playbook_id: str):
    result = toggle_playbook(playbook_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Playbook not found")
    return {"ok": True, "enabled": result, "state": get_state()}
