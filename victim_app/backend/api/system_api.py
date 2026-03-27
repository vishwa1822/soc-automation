from fastapi import APIRouter


router = APIRouter()


@router.get("/system-status")
def system_status():

    return {
        "soc_status": "running",
        "version": "1.0",
        "engines": [
            "honeytoken_engine",
            "enumeration_detector",
            "ml_anomaly_engine",
            "behavior_engine",
            "correlation_engine",
            "risk_engine",
            "alert_engine"
        ]
    }