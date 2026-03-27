from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from soc_ai_analyst import SOCAIAnalyst
import os

router = APIRouter()

# -------------------------
# Request Schema
# -------------------------

class SOCQuery(BaseModel):
    query: str


# -------------------------
# Initialize AI Analyst
# -------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

soc_analyst = SOCAIAnalyst(api_key=OPENAI_API_KEY)


# -------------------------
# AI SOC Investigation Endpoint
# -------------------------

@router.post("/ask-soc")
async def ask_soc(query: SOCQuery):

    try:

        result = soc_analyst.investigate(query.query)

        return {
            "status": "success",
            "query": result["query"],
            "logs_used": result["logs_used"],
            "analysis": result["analysis"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"SOC investigation failed: {str(e)}"
        )