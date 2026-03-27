from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

from logprocessor import LogProcessor


router = APIRouter()

SOC_API_KEY = "soc_secure_key_123"

log_processor = LogProcessor()


class LogEvent(BaseModel):

    timestamp: str
    source: str
    ip: str
    endpoint: str
    method: str
    status: int
    user_agent: Optional[str] = None
    username: Optional[str] = None


@router.post("/ingest-log")
def ingest_log(log: LogEvent, authorization: str = Header(None)):

    if authorization != f"Bearer {SOC_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = log_processor.process_log(log.dict())

    return {
        "message": "log processed",
        "result": result
    }