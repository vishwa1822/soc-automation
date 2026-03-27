from pydantic import BaseModel

class LogEvent(BaseModel):
    event_id: str
    timestamp: str
    user_id: str
    event_type: str
    ip_address: str
    geo_location: str
    device_id: str
    login_status: str
    mfa_status: str
    resource_accessed: str
    sensitivity_level: str
    session_id: str
    anomaly_score: float
    risk_score: int