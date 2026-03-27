from fastapi import APIRouter

from honeytokens.engine_instance import honeytoken_engine


router = APIRouter()


@router.get("/honeytokens")
def get_active_honeytokens():

    traps = honeytoken_engine.get_active_traps()

    return {
        "active_honeytokens": traps
    }


@router.get("/honeytokens/status")
def honeytoken_status():

    traps = honeytoken_engine.get_active_traps()

    return {
        "enabled": honeytoken_engine.scheduler.running,
        "active_traps": traps
    }


@router.post("/honeytokens/enable")
def enable_honeytokens():

    honeytoken_engine.scheduler.start()

    return {
        "status": "enabled"
    }


@router.post("/honeytokens/disable")
def disable_honeytokens():

    honeytoken_engine.scheduler.stop()

    return {
        "status": "disabled"
    }


@router.get("/honeytokens/triggers")
def get_trap_triggers():

    triggers = honeytoken_engine.get_trigger_history()

    return {
        "triggers": triggers
    }

