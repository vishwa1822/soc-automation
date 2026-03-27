from fastapi import APIRouter

from honeytokens.engine_instance import honeytoken_engine

router = APIRouter()


# --------------------------------
# Get all active honeytokens
# --------------------------------
@router.get("/honeytokens")
def get_active_honeytokens():

    traps = honeytoken_engine.get_active_traps()

    return {
        "active_honeytokens": traps
    }


# --------------------------------
# Endpoint traps (for victim app routing)
# --------------------------------
@router.get("/honeytokens/endpoints")
def get_endpoint_traps():

    traps = honeytoken_engine.registry.get_endpoint_traps()

    return {
        "endpoint_traps": traps
    }


# --------------------------------
# File honeytokens (fake admin files)
# --------------------------------
@router.get("/honeytokens/files")
def get_file_traps():

    traps = honeytoken_engine.registry.get_file_traps()

    return {
        "file_traps": traps
    }


# --------------------------------
# Honeytoken engine status
# --------------------------------
@router.get("/honeytokens/status")
def honeytoken_status():

    traps = honeytoken_engine.get_active_traps()

    return {
        "enabled": honeytoken_engine.scheduler.running,
        "active_traps": traps
    }


# --------------------------------
# Enable honeytokens
# --------------------------------
@router.post("/honeytokens/enable")
def enable_honeytokens():

    honeytoken_engine.scheduler.start()

    return {
        "status": "enabled"
    }


# --------------------------------
# Disable honeytokens
# --------------------------------
@router.post("/honeytokens/disable")
def disable_honeytokens():

    honeytoken_engine.scheduler.stop()

    return {
        "status": "disabled"
    }


# --------------------------------
# Trap trigger history
# --------------------------------
@router.get("/honeytokens/triggers")
def get_trap_triggers():

    triggers = honeytoken_engine.get_trigger_history()

    return {
        "triggers": triggers
    }