from sqlalchemy import Column, Integer, String, Float
from database import Base

class LogEvent(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String)
    timestamp = Column(String)
    user_id = Column(String)
    event_type = Column(String)
    ip_address = Column(String)
    geo_location = Column(String)
    device_id = Column(String)
    login_status = Column(String)
    mfa_status = Column(String)
    resource_accessed = Column(String)
    sensitivity_level = Column(String)
    session_id = Column(String)
    anomaly_score = Column(Float)
    risk_score = Column(Integer)