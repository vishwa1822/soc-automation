from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from soc_ai_analyst import SOCAIAnalyst
import os
import requests


router = APIRouter()


class SOCQuery(BaseModel):
  query: str


class IPLookup(BaseModel):
  ip: str


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

soc_analyst = SOCAIAnalyst(api_key=OPENAI_API_KEY)


@router.post("/ask-soc")
async def ask_soc(query: SOCQuery):

  try:

    result = soc_analyst.investigate(query.query)

    return {
      "status": "success",
      "query": result["query"],
      "logs_used": result["logs_used"],
      "analysis": result["analysis"],
    }

  except Exception as e:

    raise HTTPException(
      status_code=500,
      detail=f"SOC investigation failed: {str(e)}",
    )


@router.post("/ip-lookup")
async def ip_lookup(payload: IPLookup):

  ip = payload.ip.strip()

  if not ip:
    raise HTTPException(status_code=400, detail="IP address is required")

  try:
    resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
    data = resp.json()

    if data.get("status") != "success":
      raise HTTPException(status_code=400, detail="IP lookup failed")

    return {
      "ip": ip,
      "city": data.get("city"),
      "country": data.get("country"),
      "lat": data.get("lat"),
      "lon": data.get("lon"),
      "org": data.get("org"),
      "isp": data.get("isp"),
    }

  except HTTPException:
    raise

  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail=f"IP lookup failed: {str(e)}",
    )

